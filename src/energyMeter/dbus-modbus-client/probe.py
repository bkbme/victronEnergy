import logging
import struct
import time

from pymodbus.register_read_message import ReadHoldingRegistersResponse

import client
import utils

log = logging.getLogger()

device_types = []

def probe(mlist, pr_cb=None, pr_interval=10, timeout=None, filt=None):
    num_probed = 0
    found = []
    failed = []

    for m in mlist:
        try:
            modbus = client.make_client(m)
            unit = m.unit
        except:
            continue

        if not modbus:
            continue

        d = None

        for t in device_types:
            if t.methods and m.method not in t.methods:
                continue

            units = [unit] if unit > 0 else t.units

            try:
                for u in units:
                    mm = m._replace(unit=u)

                    if filt and not filt(mm):
                        continue

                    t0 = time.time()
                    d = t.probe(mm, modbus, timeout)
                    t1 = time.time()
                    if d:
                        break
            except:
                break

            if d:
                log.info('Found %s at %s', d.model, d)
                d.latency = t1 - t0
                d.timeout = max(d.min_timeout, d.latency * 4)
                found.append(d)
                break

        if not d:
            failed.append(m)

        modbus.put()
        num_probed += 1

        if pr_cb:
            if d or num_probed == pr_interval:
                pr_cb(num_probed, d)
                num_probed = 0

    if pr_cb and num_probed:
        pr_cb(num_probed, None)

    return found, failed

def add_handler(devtype):
    if devtype not in device_types:
        device_types.append(devtype)

def get_attrs(attr, method):
    a = []

    for t in device_types:
        if method in t.methods:
            a += getattr(t, attr, [])

    return set(a)

def get_units(method):
    return get_attrs('units', method)

def get_rates(method):
    return get_attrs('rates', method)

class ModelRegister(object):
    def __init__(self, reg, models, **args):
        self.reg = reg
        self.models = models
        self.timeout = args.get('timeout', 1)
        self.methods = args.get('methods', [])
        self.units = args.get('units', [])
        self.rates = args.get('rates', [])

    def probe(self, spec, modbus, timeout=None):
        with modbus, utils.timeout(modbus, timeout or self.timeout):
            if not modbus.connect():
                raise Exception('connection error')
            rr = modbus.read_holding_registers(self.reg.base, self.reg.count,
                unit=spec.unit)

        if not isinstance(rr, ReadHoldingRegistersResponse):
            log.debug('%s: %s', modbus, rr)
            return None

        self.reg.decode(rr.registers)
        if self.reg.value in self.models:
            m = self.models[self.reg.value]
            return m['handler'](spec, modbus, m['model'])

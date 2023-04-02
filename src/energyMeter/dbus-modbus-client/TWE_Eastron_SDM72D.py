# VenusOS module for support of Eastron SDM72D-Modbus v2
# might work also with other Eastron devices > Product code on 0xfc02 (type u16b) to be added into models overview
# 
# Community contribution by Thomas Weichenberger
# Version 1.4 - 2022-02-13
#
# Thanks to Victron for their open platform and especially for the support of Matthijs Vader
# For any usage a donation to seashepherd.org with an amount of 5 USD/EUR/GBP or equivalent is expected

import logging
import TWE_Eastron_device as device
import probe
from register import *

log = logging.getLogger()

class Reg_f32b(Reg_num):
    def __init__(self, base, *args, **kwargs):
        super(Reg_f32b, self).__init__(base, 2, *args, **kwargs)
        self.coding = ('>f', '>2H')
        self.scale = float(self.scale)

nr_phases = [ 0, 1, 3, 3 ]

phase_configs = [
    'undefined',
    '1P',
    '3P.1',
    '3P.n',
]

class Eastron_SDM72Dv2(device.EnergyMeter):
    productid = 0xb023 # id assigned by Victron Support
    productname = 'Eastron SDM72Dv2'
    min_timeout = 0.5

    def __init__(self, *args):
        super(Eastron_SDM72Dv2, self).__init__(*args)

        self.info_regs = [
            Reg_u16(0xfc02, '/HardwareVersion'),
            Reg_u16(0xfc03, '/FirmwareVersion'),
            Reg_f32b(0x000a, '/PhaseConfig', text=phase_configs, write=(0, 3)),
            Reg_u32b(0x0014, '/Serial'),
        ]

    def phase_regs(self, n):
        s = 0x0002 * (n - 1)
        regs = [
            Reg_f32b(0x0000 + s, '/Ac/L%d/Voltage' % n,        1, '%.1f V'),
            Reg_f32b(0x0006 + s, '/Ac/L%d/Current' % n,        1, '%.1f A'),
            Reg_f32b(0x000c + s, '/Ac/L%d/Power' % n,          1, '%.1f W'),
            Reg_f32b(0x015a + s, '/Ac/L%d/Energy/Forward' % n, 1, '%.1f kWh'),
            Reg_f32b(0x0160 + s, '/Ac/L%d/Energy/Reverse' % n, 1, '%.1f kWh'),
        ]
        return regs

    def device_init(self):
        self.read_info()

        phases = nr_phases[int(self.info['/PhaseConfig'])]
		
        regs = [
             Reg_f32b(0x0034, '/Ac/Power',          1, '%.1f W'),
             Reg_f32b(0x0030, '/Ac/Current',        1, '%.1f A'),
             Reg_f32b(0x0046, '/Ac/Frequency',      1, '%.1f Hz'),
             Reg_f32b(0x0048, '/Ac/Energy/Forward', 1, '%.1f kWh'),
             Reg_f32b(0x004a, '/Ac/Energy/Reverse', 1, '%.1f kWh'),
#            Reg_f32b(0x004a, '/Ac/Energy/Exported/Active', 1, '%.1f kWh'),
#            Reg_f32b(0x0048, '/Ac/Energy/Imported/Active', 1, '%.1f kWh'),
#            Reg_f32b(0x018c, '/Ac/Energy/Net',     1, '%.1f kWh'),
#	    Reg_f32b(0x0156, '/Ac/Energy/Total',   1, '%.1f kWh'),
        ]

        for n in range(1, phases + 1):
            regs += self.phase_regs(n)

        self.data_regs = regs

    def get_ident(self):
        return 'cg_%s' % self.info['/Serial']

# identifier to be checked, if register identical on all SDM630 (only first 16 bytes in u16b of 32 bit register 0xfc02)
models = {
    137: {
        'model':    'SDM72DMv2',
        'handler':  Eastron_SDM72Dv2,
    },
    135: {
        'model':    'SDM72Dv2',
        'handler':  Eastron_SDM72Dv2,
    },
}

#TCP-IP LAN Access
#probe.add_handler(probe.ModelRegister(0xfc02, models,
#                                      methods=['tcp'],
#                                      units=[1]))

#USB Access
probe.add_handler(probe.ModelRegister(Reg_u16(0xfc02), models, 
	          methods=['rtu'],
		  units=[1],
		  rates=[19200]))

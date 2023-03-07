from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import device
import probe
from register import *

class EM340_Meter(device.EnergyMeter):
  productid = 0x01
  productname = 'EM340'
  min_timeout = 0.1

  def __init__(self, *args):
    super(EM340_Meter, self).__init__(*args)
    self.info_regs = []

  def get_ident(self):
    return 'cg_et340'

  def device_init(self):
    regs = [                                                               
            Reg_s32l(0x0028, '/Ac/Power',          10, '%.1f W'),              
            Reg_u16( 0x0033, '/Ac/Frequency',      10, '%.1f Hz'),             
            Reg_s32l(0x0034, '/Ac/Energy/Forward', 10, '%.1f kWh'),            
            Reg_s32l(0x004e, '/Ac/Energy/Reverse', 10, '%.1f kWh'),            
            Reg_s32l(0x0000 + 0, '/Ac/L1/Voltage',        10, '%.1f V'),  
            Reg_s32l(0x000c + 0, '/Ac/L1/Current',      1000, '%.1f A'),  
            Reg_s32l(0x0012 + 0, '/Ac/L1/Power',          10, '%.1f W'),  
            Reg_s32l(0x0040 + 0, '/Ac/L1/Energy/Forward', 10, '%.1f kWh'),
            Reg_s32l(0x0000 + 4, '/Ac/L2/Voltage',        10, '%.1f V'),  
            Reg_s32l(0x000c + 4, '/Ac/L2/Current',      1000, '%.1f A'),  
            Reg_s32l(0x0012 + 4, '/Ac/L2/Power',          10, '%.1f W'),  
            Reg_s32l(0x0040 + 4, '/Ac/L2/Energy/Forward', 10, '%.1f kWh'),
            Reg_s32l(0x0000 + 2, '/Ac/L3/Voltage',        10, '%.1f V'),  
            Reg_s32l(0x000c + 2, '/Ac/L3/Current',      1000, '%.1f A'),  
            Reg_s32l(0x0012 + 2, '/Ac/L3/Power',          10, '%.1f W'),  
            Reg_s32l(0x0040 + 2, '/Ac/L3/Energy/Forward', 10, '%.1f kWh'),

          ]
    self.data_regs = regs

models = {
  345: {
    'model': 'ET340-DIN AV2 3 X S1 X',
    'handler': EM340_Meter,
  }
}

probe.add_handler(probe.ModelRegister(Reg_u16(0x000b), models, 
	          methods=['rtu'],
		  units=[1],
		  rates=[115200]))


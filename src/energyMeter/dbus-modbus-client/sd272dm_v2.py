from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import device
import probe
from register import *

class SDM272DM_V2_Meter(device.EnergyMeter):
  productid = 0x0089
  productname = 'SDM272DM-V2'
  min_timeout = 0.5

  def __init__(self, *args):
    super(SDM272DM_V2_Meter, self).__init__(*args)
    self.info_regs = [
        Reg_u32b(0xfc00, '/Serial'),
    ]

  def get_ident(self):
    return 'cg_sd272dm'

  def device_init(self):
    regs = [                                                               
            Reg_f32b(0x0034, '/Ac/Power',           1, '%.1f W', rfc=4),              
            Reg_f32b(0x0030, '/Ac/Current',         1, '%.1f A', rfc=4),              
            Reg_f32b(0x0046, '/Ac/Frequency',       1, '%.1f Hz', rfc=4),             
            #Reg_f32b(0x00e0, '/Ac/NeutralCurrent',  1, '%.1f Hz', rfc=4),             
            Reg_f32b(0x0048, '/Ac/Energy/Forward',  1, '%.1f kWh', rfc=4),            
            Reg_f32b(0x004a, '/Ac/Energy/Reverse',  1, '%.1f kWh', rfc=4),            
            Reg_f32b(0x0156, '/Ac/Energy/Total',    1, '%.1f kWh', rfc=4),            
            Reg_f32b(0x018C, '/Ac/Energy/Net',      1, '%.1f kWh', rfc=4),            
            Reg_f32b(0x0000 + 0, '/Ac/L1/Voltage',  1, '%.1f V', rfc=4),  
            Reg_f32b(0x0006 + 0, '/Ac/L1/Current',  1, '%.1f A', rfc=4),  
            Reg_f32b(0x000c + 0, '/Ac/L1/Power',    1, '%.1f W', rfc=4),  
            #Reg_f32b(0x0012 + 0, '/Ac/L1/ApparentPower',    1, '%.1f W', rfc=4),  
            #Reg_f32b(0x0018 + 0, '/Ac/L1/ReactivePower',    1, '%.1f W', rfc=4),  
            #Reg_f32b(0x001e + 0, '/Ac/L1/PowerFactor',    1, '%.1f W', rfc=4),  
            Reg_f32b(0x0000 + 2, '/Ac/L2/Voltage',  1, '%.1f V', rfc=4),  
            Reg_f32b(0x0006 + 2, '/Ac/L2/Current',  1, '%.1f A', rfc=4),  
            Reg_f32b(0x000c + 2, '/Ac/L2/Power',    1, '%.1f W', rfc=4),  
            #Reg_f32b(0x0012 + 4, '/Ac/L2/ApparentPower',    1, '%.1f W', rfc=4),  
            #Reg_f32b(0x0018 + 4, '/Ac/L2/ReactivePower',    1, '%.1f W', rfc=4),  
            #Reg_f32b(0x001e + 4, '/Ac/L2/PowerFactor',    1, '%.1f W', rfc=4),  
            Reg_f32b(0x0000 + 4, '/Ac/L3/Voltage',  1, '%.1f V', rfc=4),  
            Reg_f32b(0x0006 + 4, '/Ac/L3/Current',  1, '%.1f A', rfc=4),  
            Reg_f32b(0x000c + 4, '/Ac/L3/Power',    1, '%.1f W', rfc=4),  
            #Reg_f32b(0x0012 + 2, '/Ac/L3/ApparentPower',    1, '%.1f W', rfc=4),  
            #Reg_f32b(0x0018 + 2, '/Ac/L3/ReactivePower',    1, '%.1f W', rfc=4),  
            #Reg_f32b(0x001e + 2, '/Ac/L3/PowerFactor',    1, '%.1f W', rfc=4),  

          ]
    self.data_regs = regs

models = {
  0x0089: {
    'model': 'Eastron SDM72DM-V2',
    'handler': SDM272DM_V2_Meter,
  }
}

probe.add_handler(probe.ModelRegister(Reg_u16(0xfc02), models, 
	          methods=['rtu'],
		  units=[1],
		  rates=[19200]))


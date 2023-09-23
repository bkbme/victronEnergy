from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import device
import probe
from register import *

class SDM272DM_V2_Meter(device.CustomName, device.EnergyMeter):
  productid = 0x0089
  productname = 'SDM272DM-V2'
  min_timeout = 0.5

  def __init__(self, *args):

    self.info_regs = [
        Reg_u32b(0xfc00, '/Serial'),
    ]
    self.switch_phase_2_3 = True
    self.nr_phases = 3

    super(SDM272DM_V2_Meter, self).__init__(*args)

  def get_ident(self):
    return 'cg_sd272dm'

  def device_init(self):
    regs = [                                                               
            Reg_f32b(0x0034, '/Ac/Power',           1, '%.1f W', rfc=4),              
            Reg_f32b(0x0046, '/Ac/Frequency',       1, '%.1f Hz', rfc=4),              
            Reg_f32b(0x0048, '/Ac/Energy/Forward',  1, '%.1f kWh', rfc=4),            
            Reg_f32b(0x004a, '/Ac/Energy/Reverse',  1, '%.1f kWh', rfc=4),            
            Reg_f32b(0x0000 + 0, '/Ac/L1/Voltage',  1, '%.1f V', rfc=4),  
            Reg_f32b(0x0006 + 0, '/Ac/L1/Current',  1, '%.1f A', rfc=4),  
            Reg_f32b(0x000c + 0, '/Ac/L1/Power',    1, '%.1f W', rfc=4),  
          ]
            
    phase = 2 if not self.switch_phase_2_3 else 3
    regs.extend([
      Reg_f32b(0x0000 + 2, f'/Ac/L{phase}/Voltage',  1, '%.1f V', rfc=4),  
      Reg_f32b(0x0006 + 2, f'/Ac/L{phase}/Current',  1, '%.1f A', rfc=4),  
      Reg_f32b(0x000c + 2, f'/Ac/L{phase}/Power',    1, '%.1f W', rfc=4),  
    ])

    phase = 3 if not self.switch_phase_2_3 else 2
    regs.extend([
      Reg_f32b(0x0000 + 4, f'/Ac/L{phase}/Voltage',  1, '%.1f V', rfc=4),  
      Reg_f32b(0x0006 + 4, f'/Ac/L{phase}/Current',  1, '%.1f A', rfc=4),  
      Reg_f32b(0x000c + 4, f'/Ac/L{phase}/Power',    1, '%.1f W', rfc=4),  
    ])

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


from pysnmp import debug
from snmp_util.reference.device_info import device_info as mdi 
from snmp_util.reference.brand_parser import brand_parser as brand_parser 

# debug.setLogger(debug.Debug('dsp', 'msgproc', 'secmod','mibbuild'))
class main_device_info:
    def __init__(self,ip_address  = None, community_string = None):
        self.ip_address = ip_address
        self.community_string = community_string

    def run(self):
        mdi_runner = mdi(self.ip_address,self.community_string)
        raw_info = mdi_runner.run()
        if raw_info["is_valid"]:
            bp_runner = brand_parser(raw_info["device_info"])
            main_info = bp_runner.run()
            main_info["ip_address"] = self.ip_address
            return {'is_valid': True , 'main_info' : main_info}
        else:
            return {'is_valid': False , 'main_info' : {}}

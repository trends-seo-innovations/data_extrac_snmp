from pysnmp import hlapi
import sys
    
import json

class main_device_details:
    def __init__(self, device_ip = None, oid_list = None, snmp_community_string = 'public'):
        self.device_ip = device_ip
        self.oid_list = oid_list
        self.snmp_community_string = snmp_community_string
        # self.oid_file = None

    def cast_value(self, value):
        try:
            return int(value)
        except (ValueError, TypeError):
            try:
                return float(value)
            except (ValueError, TypeError):
                try:
                    return str(value)
                except (ValueError, TypeError):
                    pass
        return value

    def cast_oid(self,oid):
        oid_dict = self.oid_list["oid_list"]
        return list(oid_dict[0].keys())[list(oid_dict[0].values()).index(oid)]

    def construct_object_types(self , list_of_oids):
        object_types = []
        for oid in list_of_oids:
            object_types.append(hlapi.ObjectType(hlapi.ObjectIdentity(oid)))
        return object_types

    def fetch(self, handler, count):
        result = None
        for i in range(count):
            try:
                error_indication, error_status, error_index, var_binds = next(handler)
                if not error_indication and not error_status:
                    items = {}
                    for var_bind in var_binds:
                        items[self.cast_oid(str(var_bind[0])) ] = self.cast_value(var_bind[1])
                    result = items
                else: 
                    raise RuntimeError('Got SNMP error: {0}'.format(error_indication))
            except SystemError:
                return {'error' : "No SNMP Response",'is_valid' : False}
        return result

    def get(self,target, oids, credentials, port=161, engine=hlapi.SnmpEngine(), context=hlapi.ContextData()):
        handler = hlapi.getCmd(
            engine,
            credentials,
            hlapi.UdpTransportTarget((target, port)),
            context,
            *self.construct_object_types(oids)
        )
        return self.fetch(handler, 1)

    def get_bulk(self,target, oids, credentials, count, start_from=0, port=161,engine=hlapi.SnmpEngine(), context=hlapi.ContextData()):
        handler = hlapi.bulkCmd(
            engine,
            credentials,
            hlapi.UdpTransportTarget((target, port)),
            context,
            start_from, count,  
            *self.construct_object_types(oids)
        )
        return self.fetch(handler, count)

    def run(self):
        try:
            device_info = list()
            for value in self.oid_list["oid_list"]:
                for v,k in value.items():
                    device_info.append(k)
            return self.get(self.device_ip,device_info, hlapi.CommunityData(self.snmp_community_string))
        except Exception as err:
            raise ValueError(err)
       
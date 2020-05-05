import sys
from pysnmp.hlapi import *
import configparser
import getopt
import json
import logging
import os
import re
import sys




class device_info:
    def __init__(self, ip_interface = None ,community_string = None):
        self.community_string = community_string
        self.ip_interface = ip_interface
        #Do not alter any of this
        self.cdpCacheDeviceId = '.1.3.6.1.4.1.9.9.23.1.2.1.1.6'
        self.cdpCacheDevicePort = '.1.3.6.1.4.1.9.9.23.1.2.1.1.7'
        self.cdpCachePlatform = '.1.3.6.1.4.1.9.9.23.1.2.1.1.8'
        self.sysname = '.1.3.6.1.2.1.1.5.0'
        self.sysDesc = '.1.3.6.1.2.1.1.1.0'
        #end

    #option 1 nextcommand
    # def run(self):
    #     for (errorIndication, errorStatus, errorIndex, varBinds) in nextCmd(
    #         SnmpEngine(),
    #         CommunityData(self.community_string),
    #         UdpTransportTarget((self.ip_interface, 161)),
    #         ContextData(),
    #         ObjectType(ObjectIdentity(self.cdpCacheDeviceId)),
    #         ObjectType(ObjectIdentity(self.cdpCacheDevicePort)),
    #         ObjectType(ObjectIdentity(self.cdpCachePlatform)),
    #         lookupMib=False,
    #         lexicographicMode=False
    #     ):
    #         if errorIndication or errorStatus or errorIndex:
    #             return None
    #     device_info = {
    #         'system_name': re.findall(r'([^(\n]+).*', str(varBinds[0][1]))[0],
    #         'system_description': str(varBinds[2][1])
    #         }
    #     return device_info

    def run(self):
        is_valid = True
        device_info = {
                    'system_name': '',
                    'system_description': ''
                }
        for (errorIndication, errorStatus, errorIndex, varBinds)  in getCmd(
            SnmpEngine(),
            CommunityData(self.community_string),
            UdpTransportTarget((self.ip_interface, 161)),
            ContextData(),
            ObjectType(ObjectIdentity(self.sysname)),
            ObjectType(ObjectIdentity(self.sysDesc))
            ):
            if errorIndication:
                is_valid= False
            elif errorStatus:
                is_valid= False
            else:
                device_info = {
                    'system_name': str(varBinds[0][1]),
                    'system_description': str(varBinds[1][1])
                }
            return {'is_valid': is_valid , 'device_info': device_info }


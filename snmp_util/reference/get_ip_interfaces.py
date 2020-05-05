import scapy.all as scapy


class get_ip_interfaces:
    def __init__(self,ip_range):
        self.ip_range = ip_range

    def scan(self):
        print(self.ip_range)
        try:
            packets = scapy.ARP(pdst = self.ip_range)
            bcast_packets = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff")
            arp_bcast_packets = bcast_packets / packets
            answered_list = scapy.srp(arp_bcast_packets,timeout = 1, verbose = False)[0]
            client_list = list()
            for element in answered_list:
                client_dict = {'ip' : element[1].psrc , "mac" : element[1].hwsrc}
                client_list.append(client_dict)
            return client_list
        except Exception as identifier:
            return []

    def run(self):
        scan_list = self.scan()
        ip_list = list()
        for client in scan_list:
            ip_list.append(client["ip"])
        return ip_list
            

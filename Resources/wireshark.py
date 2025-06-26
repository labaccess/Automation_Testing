import subprocess
import pyshark
from tqdm import tqdm

import re

global TARGET_DOMAIN, DNS_DISPLAY_FILTER

DNS_DISPLAY_FILTER = 'dns and dns.qry.name contains "filgoal"'
TARGET_DOMAIN = 'www.filgoal2.com'

class WiresharkSession:
    def __init__(self,interface_match,display_match=None):
        self.match_interface = interface_match
        self.interface_wireshark = self.list_interfaces(self.match_interface)
        if display_match is None :
            self.display_filter = DNS_DISPLAY_FILTER
        else:
            self.display_filter = display_match

        self.cap = pyshark.LiveCapture(interface=self.interface_wireshark , display_filter=self.display_filter)

    def list_interfaces(self,reg_match):
        result = subprocess.run(['tshark', '-D'], capture_output=True, text=True)
        print("we will select WIFI interface in wireshark list")
        for idx, line in enumerate(result.stdout.strip().split('\n')):
            print(f"{idx}: {line}")
            if reg_match in line:
                INTERFACE_WIRESHARK = line.split(' ', 1)[1].split('(')[0].strip()
                break

        return INTERFACE_WIRESHARK

    def wireshark_dns_live_stream(self,target_domain=TARGET_DOMAIN,display_filter=DNS_DISPLAY_FILTER):
        print(f"Listening for DNS queries to {target_domain}...")
        print(f"Starting capture on interface: {self.interface_wireshark}")
        
        self.cap.sniff(timeout=0)
        print(f"Captured {len(self.cap)} packets. Scanning for DNS query to {target_domain}...\n")
        print("Captured packets:")

        for pkt in self.cap:
            # index = index+ 1
            # print(f"analysis packet number {index}")
            print(pkt)
            try:
                if 'DNS' in pkt and hasattr(pkt.dns, 'qry_name'):
                    dns_query = pkt.dns.qry_name.lower()
                    if dns_query == target_domain:
                        print(f"[{pkt.sniff_time}] Matched Query:")
                        if hasattr(pkt, 'ip'):
                            print(f"    Source IP: {pkt.ip.src}")
                            print(f"    Destination IP: {pkt.ip.dst}")
                        elif hasattr(pkt, 'ipv6'):
                            print(f"    Source IP: {pkt.ipv6.src}")
                            print(f"    Destination IP: {pkt.ipv6.dst}")
                        break  # Exit after first match
            except AttributeError as Error:
                print(f"Error is {Error}")
                print(f"Error is {pkt}")
                continue
            except Exception as Error:
                print(f"Normal Error is {Error}")
                print(f"Normal Error is {pkt}")
                continue

    
if __name__ == "__main__":
    sample = WiresharkSession("Wi-Fi")
    sample.wireshark_dns_live_stream()
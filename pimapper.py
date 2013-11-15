#!/usr/bin/python

import nmap
import sys
from netaddr import IPNetwork
from includes.settings import bcolors
from includes.database import *
from includes.network import network
import time

primaryIf = 'en1'

netinfo = network()

currentIP = '172.16.10.0'
#currentIP = commands.getoutput("/sbin/ifconfig").split("\n")[1].split()[1][5:]
currentCIDR = '24'
#currentCIDR = IPChecks.getBits(IPChecks.get_netmask(primaryIf))
currentPreRange = currentIP + "/" + str(currentCIDR)
ip2 = IPNetwork(currentPreRange)
currentRange = str(ip2.network) + "/" + str(currentCIDR)

now = time.strftime('%Y-%m-%d %H:%M:%S')

nm = nmap.PortScannerAsync()

raw_input('Your current scan range is ' + currentRange + '. Press enter to start the scan:')

def callback_result(host_ip, scan_result):
    #Check if host is up
    try:
        scan_result['scan'][host_ip]['status']['state'] == 'up'
    except:
        pass
    else:
        #Assign variable to array value
        print scan_result['scan'][host_ip]['hostname']
        print host_ip

        #Get MAC address for host and check if exists in DB
        #current.get(current.macAddress)
        for query_return in current.select(current.macAddress == netinfo.getmac(host_ip)):
                if query_return.macAddress != netinfo.getmac(host_ip):
                    write_mac_db(netinfo.getmac(host_ip), now)
                    break
                else:
                    pass



print bcolors.HEADER + 'Starting pimapper discovery scan' + bcolors.ENDC

nm.scan(hosts=currentRange, arguments='-sP', callback=callback_result)

while nm.still_scanning():
    time.sleep(0.1)
    sys.stdout.write("-")
    sys.stdout.flush()
print bcolors.HEADER + '\nScan complete' + bcolors.ENDC


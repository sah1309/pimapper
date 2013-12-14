#!/usr/bin/python

import nmap
import socket
import sys
from netaddr import IPNetwork
from includes.settings import bcolors
from includes.database import *
from includes.network import network
import time

primaryIf='eth0'

IPChecks = network()

currentIP = "172.16.10.0"
currentCIDR = "24"
#currentIP = commands.getoutput("/sbin/ifconfig").split("\n")[1].split()[1][5:]
#currentCIDR = IPChecks.getBits(IPChecks.get_netmask(primaryIf))
currentPreRange = currentIP + "/" + str(currentCIDR)
ip2 = IPNetwork(currentPreRange)
currentRange = str(ip2.network) + "/" + str(currentCIDR)

timestamp = int(time.time())

discover = nmap.PortScannerAsync()

useCurrent = raw_input('Your current IP range is ' + currentRange + '. Would you like to map that? [yes/no]: ')
if useCurrent == 'yes':
        scanRange = currentRange
else:
        scanRange = raw_input('Please enter your scan range in CIDR format: ')

if IPChecks.subnetCheck(currentIP, scanRange) == False:
        print bcolors.WARNING + 'This subnet is outside your own, MAC Address gathering is disabled' + bcolors.ENDC
else:
        print bcolors.OKGREEN + 'MAC Address gathering enabled!' + bcolors.ENDC
        macEnable = True

#This is here for testing!
macEnable = False

def discovery_scan(host, scan_result):
        addMac = True
        added = False
        try:
                scan_result['scan'][host]['status']['state'] == 'up'
        except:
                pass
        else:        

                #Check if hostname has been found
                if scan_result['scan'][host]['hostname'] == "":
                    try:
                        #Try secondary means of getting hostname
                        hostnameNice = socket.gethostbyaddr(host)
                    except:
                        #Insert data into liveIP tables
                        print bcolors.OKGREEN + 'Found Live IP ' + bcolors.ENDC + '( ' + host + ' )'
                        live_ip.create(ipaddress=host, scanTime=timestamp)
                else:
                    hostnameNice = scan_result['scan'][host]['hostname']
                    for i in host_current.select().where(host_current.hostname == hostnameNice):
                        #If the hostname is there, but IP has changed...
                        if i.hostname == hostnameNice and i.hostIP != host:
                            hostUpdate = host_current.update(hostIP=host, scanTime=timestamp).where(host_current.hostname == hostnameNice)
                            hostUpdate.execute()
                            print bcolors.OKBLUE + 'Existing Host Updated' + bcolors.ENDC + '( ' + hostnameNice + ' - ' + host + ' )'
                            added = True
                        #If the hostname and IP address match
                        elif i.hostname == hostnameNice and i.hostIP == host:
                            print bcolors.OKGREEN + 'Existing Host Found' + bcolors.ENDC + '( ' + hostnameNice + ' - ' + host + ' )'
                            hostUpdate = host_current.update(scanTime=timestamp).where(host_current.hostname == hostnameNice)
                            hostUpdate.execute()
                            added = True
                        #If the hostname is not in the list at all
                    if added == True:
                        pass
                    else:
                        host_current.create(hostname=hostnameNice, hostIP=host, scanTime=timestamp)
                        print bcolors.WARNING + 'New Host Found' + bcolors.ENDC + '( ' + hostnameNice + ' - ' + host + ' )'

                
                if macEnable == True:
                                macAddress=IPChecks.getMac(host)
                                if macAddress:
                                                for m in mac.select().where(mac.hostname == hostnameNice):
                                                        if m.macAddr == macAddress:
                                                                addMac = False
                                                                pass
                                                if addMac == True:
                                                        mac.create(
                                                                hostname=hostnameNice,
                                                                macAddr=macAddress,
                                                                scanTime=timestamp,
                                                        )
                                                        print bcolors.OKGREEN + 'MAC address stored ' + bcolors.ENDC + '( ' + hostnameNice + ' - ' + macAddress + ' )'





print bcolors.HEADER + 'Starting pimapper discovery scan' + bcolors.ENDC

discover.scan(hosts='172.16.10.101', arguments='-sP', callback=discovery_scan)

while discover.still_scanning():
        time.sleep(0.5)
        sys.stdout.write("-")
        sys.stdout.flush()
print bcolors.HEADER + '\nDiscovery scan complete' + bcolors.ENDC

print bcolors.HEADER + 'Starting basic services scan' + bcolors.ENDC

port_scan = nmap.PortScanner()
for i in host_current.select(host_current.hostIP).where(host_current.scanTime == timestamp):
    print bcolors.OKGREEN + 'Scanning: ' + i.hostIP + bcolors.ENDC
    port_scan.scan(i.hostIP, '22-443')

    for service in port_scan[i.hostIP].all_tcp():
            print 'Port: ' + str(service) + ' - ' + ports.get(ports.port == service).description

    print IPChecks.nmapScan(i, 'lan')
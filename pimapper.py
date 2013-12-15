#!/usr/bin/python

import nmap
import socket
import sys
import commands
import json
from netaddr import IPNetwork
from includes.settings import bcolors
from includes.database import *
from includes.network import network
import time

primaryIf='eth0'
IPChecks = network()
#currentIP = "172.16.10.0"
#currentCIDR = "24"
currentIP = commands.getoutput("/sbin/ifconfig").split("\n")[1].split()[1][5:]
currentCIDR = IPChecks.getBits(IPChecks.get_netmask(primaryIf))
currentPreRange = currentIP + "/" + str(currentCIDR)
ip2 = IPNetwork(currentPreRange)
currentRange = str(ip2.network) + "/" + str(currentCIDR)
timestamp = int(time.time())

print bcolors.OKGREEN
print "   _____ _                       __  __              "
print "  / ____| |                     |  \/  |             "
print " | (___ | |_ ___  _ __ _ __ ___ | \  / | __ _ _ __   "
print "  \___ \| __/ _ \| '__| '_ ` _ \| |\/| |/ _` | '_ \  "
print "  ____) | || (_) | |  | | | | | | |  | | (_| | |_) | "
print " |_____/ \__\___/|_|  |_| |_| |_|_|  |_|\__,_| .__/  "
print "                                             | |     "
print "                                             |_|     "
print bcolors.ENDC
print ' -- Navigate to http://' + currentIP + '/stormmap.py'
print ' -- '
print ' -- A program with various options to map your LAN'
print ' --'
print ' -- Optional arguments'
print ' -h --help               Show this help message'
print ' -wl --watch-list        List watched targets'
print ' -wt --watch-host        Set watch host'
print ' -ws --watch-subnet      Set watch subnet'
print ' -wr --watch-remove      Remove watched target'
print
useCurrent = raw_input('Your current IP range is ' + currentRange + '. Would you like to map that? [yes/no]: ')
if useCurrent == 'yes':
        scanRange = currentRange
else:
        scanRange = raw_input('Please enter a single host or scan range in CIDR notation: ')

if IPChecks.subnetCheck(currentIP, scanRange) == False:
        print bcolors.WARNING + 'This subnet is outside your own, MAC Address gathering is disabled' + bcolors.ENDC
else:
        print bcolors.OKGREEN + 'MAC Address gathering enabled!' + bcolors.ENDC
        macEnable = True

def discovery_scan(host, scan_result):
        addMac = True
        added = False
        try:
                scan_result['scan'][host]['status']['state'] == 'up'
        except:
                pass
        else:
                if IPChecks.subnetCheck(host, currentRange) == True:
                    macEnable = True
                    try:
                        ms=IPChecks.getMac(host)
                        macsuffix='-' + ms[12:]
                    except:
                        macsuffix=''

                    #Check if hostname has been found
                    hostnametemp = scan_result['scan'][host]['hostname']
                    if hostnametemp == "":
                        try:
                            hostnameNice = socket.gethostbyaddr(host) + macsuffix
                        except:
                            hostnameNice = host + macsuffix
                    else:
                        hostnameNice = scan_result['scan'][host]['hostname'] + macsuffix
                else:
                    #Check if hostname has been found
                    macEnable = False
                    hostnametemp = scan_result['scan'][host]['hostname']
                    if hostnametemp == "":
                        try:
                            hostnameNice = socket.gethostbyaddr(host) + '- remote'
                        except:
                            hostnameNice = host + '- remote'
                    else:
                        hostnameNice = scan_result['scan'][host]['hostname'] + '- remote'

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
                        for m in mac_address.select().where(mac_address.hostname == hostnameNice):
                            if m.macAddr == macAddress:
                                addMac = False
                                pass
                        if addMac == True:
                            mac_address.create(
                                hostname=hostnameNice,
                                macAddr=macAddress,
                                scanTime=timestamp,
                            )
                            print bcolors.OKGREEN + 'MAC address stored ' + bcolors.ENDC + '( ' + hostnameNice + ' - ' + macAddress + ' )'





print bcolors.HEADER + 'Starting pimapper discovery scan' + bcolors.ENDC

discover = nmap.PortScannerAsync()
discover.scan(hosts=scanRange, arguments='-sP', callback=discovery_scan)

while discover.still_scanning():
        time.sleep(0.5)
        sys.stdout.write("-")
        sys.stdout.flush()

print
print bcolors.HEADER + 'Starting basic services scan' + bcolors.ENDC

service_scanner = nmap.PortScannerAsync()
def callback_result(host, scan_result):
    if host in scan_result['scan']:
        if 'tcp' in scan_result['scan'][host]:
            portresults = scan_result['scan'][host]['tcp']
            for service in portresults:
                print bcolors.OKGREEN + 'Found open port: ' + str(service) + ' (' + ports.get(ports.port == service).description + ')' + bcolors.ENDC
                host_id = host_current.get(host_current.hostIP == host).id
                services.create(hostID=host_id, portID=service, scanTime=timestamp)

for i in host_current.select(host_current.hostIP, host_current.hostname).where(host_current.scanTime == timestamp):
    print bcolors.OKBLUE + 'Scanning ' + i.hostname + ' - ' + i.hostIP + '....' + bcolors.ENDC
    service_scanner.scan(hosts=i.hostIP, ports='22-2222', arguments='', callback=callback_result)
    while service_scanner.still_scanning():
        time.sleep(0.3)
        sys.stdout.write("-")
        sys.stdout.flush()

    host_id = host_current.get(host_current.hostname == i.hostname).id
    print bcolors.OKBLUE + 'Trying to discover OS for ' + i.hostname + '....' + bcolors.ENDC
    hostOS = IPChecks.os_match(i.hostIP, 'lan')
    if hostOS[1] == '0':
        print bcolors.OKGREEN + 'Identified ' + i.hostname + ' as ' + hostOS[0] + bcolors.ENDC
        os_match.create(hostID=host_id, os=hostOS[0], confidence='100', scanTime=timestamp)
    elif hostOS[0] == 'Unknown':
        print bcolors.OKGREEN + 'Unable to identify OS for ' + i.hostname + bcolors.ENDC
    else:
        print bcolors.OKGREEN + 'Identified ' + i.hostname + ' as ' + hostOS[0] + ' with a confidence of ' + hostOS[1] + '%' + bcolors.ENDC
        os_match.create(hostID=host_id, os=hostOS[0], confidence=hostOS[1], scanTime=timestamp)


print 'Creating report..'
results = dict()

for i in host_current.select(host_current.id, host_current.hostIP, host_current.hostname).where(host_current.scanTime == timestamp):
    os = os_match.get(os_match.hostID == i.id, os_match.scanTime == timestamp)
    results[i.hostname] = {'ip' : i.hostIP, 'os' : {'type' : os.os, 'confidence': os.confidence}}
    for portresults in services.select(services.hostID, services.portID).where(services.scanTime == timestamp):
        if portresults.hostID == i.id:
            results[i.hostname]['scan'].update({ portresults.portID : { 'description' : ports.get(ports.port == portresults.portID).description }})

print json.dumps(results, indent=2)



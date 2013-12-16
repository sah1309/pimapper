#!/usr/bin/python


import commands
import json
from includes.settings import bcolors
from netaddr import IPNetwork
from includes.database import *
from includes.network import network
from includes.scanners import *


def create_json_report():
    print 'Creating report..'
    results = dict()
    for i in host_current.select(host_current.id, host_current.hostIP, host_current.hostname).where(host_current.scanTime == timestamp):
        os = os_match.get(os_match.hostID == i.id, os_match.scanTime == timestamp)
        results[i.hostname] = {'ip' : i.hostIP, 'os' : {'type' : os.os, 'confidence': os.confidence}}
        results[i.hostname].update({'scan':{}})
        for portresults in services.select(services.hostID, services.portID).where(services.scanTime == timestamp).where(services.hostID == i.id):
            results[i.hostname]['scan'].update({ portresults.portID : { 'description' : ports.get(ports.port == portresults.portID).description }})
    return json.dumps(results, indent=2)

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

current_scan = scanners()

current_scan.discovery_scan(scanRange)
current_scan.port_scan()
current_scan.os_fingerprint()


print bcolors.HEADER + 'Scan complete!' + bcolors.ENDC
outputJSON = raw_input(bcolors.OKBLUE + 'Type "yes" to output the report JSON to screen: ' + bcolors.ENDC)
if outputJSON == 'yes':
    print create_json_report()
else:
    print 'Quitting'
    quit()


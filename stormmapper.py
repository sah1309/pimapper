#!/usr/bin/python

import commands
import json
from includes.settings import bcolors
from netaddr import IPNetwork
from includes.database import *
from includes.network import network
from includes.scanners import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("s", help="Enter a single host or scan range in CIDR notation")
parser.add_argument("-d", "--discover", help="Perform Host Discovery Scan", action="store_true")
parser.add_argument("-o", "--os", help="Perform OS Matching", action="store_true")
parser.add_argument("-p", "--port", help="Perform Port-Scan", action="store_true")
parser.add_argument("-q", "--quiet", help="Hide scan output", action="store_true")
args = parser.parse_args()

scanRange = args.s

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
currentIP = commands.getoutput("/sbin/ifconfig").split("\n")[1].split()[1][5:]
currentRange = str(IPNetwork(currentIP + "/" + str(IPChecks.getBits(IPChecks.get_netmask(primaryIf)))).network) + "/" + str(IPChecks.getBits(IPChecks.get_netmask(primaryIf)))
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

if IPChecks.subnetCheck(currentIP, scanRange) == False:
        print bcolors.WARNING + 'This subnet is outside your own, MAC Address gathering is disabled' + bcolors.ENDC
else:
        print bcolors.OKGREEN + 'MAC Address gathering enabled!' + bcolors.ENDC
        macEnable = True

current_scan = scanners()

maxTime = []
for i in host_current.select(host_current.scanTime):
    maxTime.append(i.scanTime)
print maxTime



if args.discover:
    current_scan.discovery_scan(scanRange,timestamp)

if args.port:
    current_scan.port_scan(timestamp)

if args.os:
    current_scan.os_fingerprint(timestamp)


print bcolors.HEADER + 'Scan complete!' + bcolors.ENDC
outputJSON = raw_input(bcolors.OKBLUE + 'Type "yes" to output the report JSON to screen: ' + bcolors.ENDC)
if outputJSON == 'yes':
    print create_json_report()
else:
    print 'Quitting'
    quit()


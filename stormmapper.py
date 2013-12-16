#!/usr/bin/python

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-t", "--target", nargs='?', help="Perform Full Scan. SCAN = Single IP address or Range in CIDR notation")
parser.add_argument("-o", "--os", help="Perform OS Matching", action="store_true")
parser.add_argument("-p", "--port", help="Perform Port-Scan", action="store_true")
parser.add_argument("-q", "--quiet", help="Hide scan output", action="store_true")
parser.add_argument("--output", help="output JSON after scan", action="store_true")
args = parser.parse_args()

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

if not (args.target or args.port or args.os):
    print "Type stormmapper.py --help for options"
    print
    quit()

current_scan = scanners()

if args.target:
    current_scan.discovery_scan(args.target,timestamp)

maxTime = []
for i in host_current.select(host_current.scanTime):
    maxTime.append(i.scanTime)
lastScan = max(maxTime)

if args.port:
    current_scan.port_scan(lastScan)

if args.os:
    current_scan.os_fingerprint(lastScan)

if args.output:
    print create_json_report()
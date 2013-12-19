#!/usr/bin/python

import json, commands, logging, sys, argparse, os
from includes.settings import bcolors
from netaddr import IPNetwork
from includes.database import *
from includes.network import network
from includes.scanners import *

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--target", nargs='?', help="Perform Full Scan. SCAN = Single IP address or Range in CIDR notation")
parser.add_argument("-a", "--auto", help="Run full scan against current network", action="store_true")
parser.add_argument("-o", "--os", help="Perform OS Matching", action="store_true")
parser.add_argument("-p", "--port", help="Perform Port-Scan", action="store_true")
parser.add_argument("-q", "--quiet", help="Hide scan output", action="store_true")
parser.add_argument("--output", help="output JSON after scan", action="store_true")
args = parser.parse_args()

#Setup Logging
LOG_FILENAME = '/var/log/stormmapper.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,)

#Create pidfile
pid = str(os.getpid())
pidfile = "/var/run/stormmapper.pid"

# Check if pidfile exists
# Exit if pidfile exists
# Create pidfile if it doesnt
if os.path.isfile(pidfile):
    print "%s already exists, exiting" % pidfile
    sys.exit()
else:
    file(pidfile, 'w').write(pid)

def main():
    try:
        #  Output the latest scan in JSON format
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

        # Set primary interface name variable
        primaryIf='eth0'
        # Create network checking object
        IPChecks = network()
        # Set current IP address variable
        currentIP = commands.getoutput("/sbin/ifconfig").split("\n")[1].split()[1][5:]
        # Set current IP range in CIDR format variable
        currentRange = str(IPNetwork(currentIP + "/" + str(IPChecks.getBits(IPChecks.get_netmask(primaryIf)))).network) + "/" + str(IPChecks.getBits(IPChecks.get_netmask(primaryIf)))
        # Set current time variable
        timestamp = int(time.time())

        print bcolors.OKGREEN
        print "   _____ _                       __  __              "
        print "  / ____| |                     |  \/  |             "
        print " | (___ | |_ ___  _ __ _ __ ___ | \  / | __ _ _ __   "
        print "  \___ \| __/ _ \| '__| '_ ` _ \| |\/| |/ _` | '_ \  "
        print "  ____) | || (_) | |  | | | | | | |  | | (_| | |_) | "
        print " |_____/ \__\___/|_|  |_| |_| |_|_|  |_|\__,_| .__/  "
        print bcolors.OKBLUE + "  Network Mapping and Discovery       " + bcolors.OKGREEN + "       | |     "
        print bcolors.OKBLUE + "  Simon Beattie // @Si_Bt // 2013     " + bcolors.OKGREEN + "       |_|     "
        print bcolors.ENDC

        # If no arguements have been passed, exit program
        if not (args.target or args.port or args.os or args.auto):
            print "Type stormmapper.py --help for options"
            print
            os.unlink(pidfile)
            quit()

        # Create current scan object
        current_scan = scanners()
        # Set time of last scan ran
        maxTime = []
        for i in host_current.select(host_current.scanTime):
            maxTime.append(i.scanTime)
        lastScan = max(maxTime)
        # Run automatic scan on current IP range (this is usually triggered by web/AutoScanCron.php
        if args.auto:
            current_scan.discovery_scan(currentRange,timestamp)
            current_scan.port_scan(timestamp)
            current_scan.os_fingerprint(timestamp)
            print bcolors.OKGREEN + "Scan Completed!" + bcolors.ENDC

        # Run discovery scan on specified range (CIDR), or ip address
        if args.target:
            current_scan.discovery_scan(args.target,timestamp)
            print bcolors.OKGREEN + "Scan Completed!" + bcolors.ENDC

        # Run port-scan on all targets added or updated in last discovery scan
        if args.port:
            current_scan.port_scan(lastScan)
            print bcolors.OKGREEN + "Scan Completed!" + bcolors.ENDC

        # Run operating system scan on all targets added or updated in last discovery scan
        if args.os:
            current_scan.os_fingerprint(lastScan)
            print bcolors.OKGREEN + "Scan Completed!" + bcolors.ENDC

        # Output the latest scan in JSON format
        if args.output:
            print create_json_report()

        #Cleanup pid file
        os.unlink(pidfile)

    # Capture exits and errors
    except KeyboardInterrupt:
        print "Shutdown requested.. exiting"
        os.unlink(pidfile)
    except Exception:
        logging.exception('StormMapper Error')
        print "An error has occurred - Check the logs!"
        os.unlink(pidfile)

if __name__ == "__main__":
    main()
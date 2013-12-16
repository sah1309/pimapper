__author__ = 'simonbeattie'

import nmap
import socket
import sys
import time
import commands
from includes.settings import bcolors
from includes.network import network
from netaddr import IPNetwork
from includes.database import *

class scanners():

    def discovery_scan(self, scanRange):
        print bcolors.HEADER + 'Starting pimapper discovery scan' + bcolors.ENDC
        # Instantiate discovery scanner object
        discover = nmap.PortScannerAsync()
        # Start discovery scan, outputting to discovery_scan
        discover.scan(hosts=scanRange, arguments='-sP', callback=self.discovery_scanner)
        # Whilst scanning, output - to screen
        while discover.still_scanning():
                time.sleep(0.5)
                sys.stdout.write("-")
                sys.stdout.flush()

    def discovery_scanner(self, host, scan_result):
        IPChecks = network()

        primaryIf='eth0'
        currentIP = commands.getoutput("/sbin/ifconfig").split("\n")[1].split()[1][5:]
        currentCIDR = IPChecks.getBits(IPChecks.get_netmask(primaryIf))
        currentPreRange = currentIP + "/" + str(currentCIDR)
        ip2 = IPNetwork(currentPreRange)
        currentRange = str(ip2.network) + "/" + str(currentCIDR)
        timestamp = int(time.time())


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

    def port_scan(self):
        print bcolors.HEADER + 'Starting basic services scan' + bcolors.ENDC
        # Instantiate service port scanner object
        service_scanner = nmap.PortScannerAsync()
        # Grab list of hosts discovered during most recent scan
        for i in host_current.select(host_current.hostIP, host_current.hostname, host_current.scanTime).where(host_current.scanTime == host_current.max(host_current.scanTime)):
            print bcolors.OKBLUE + 'Scanning ' + i.hostname + ' - ' + i.hostIP + '....' + bcolors.ENDC
            # Start service port scan
            service_scanner.scan(hosts=i.hostIP, ports='22-2222', arguments='', callback=self.port_scan)
            # Whilst scanning, output - to screen
            while service_scanner.still_scanning():
                time.sleep(0.3)
                sys.stdout.write("-")
                sys.stdout.flush()

    def port_scanner(self, host, scan_result, timestamp):
        query = host_current.select(fn.Max(host_current.scanTime).alias('count'))
        for i in query:
            timestamp = i.count
        if host in scan_result['scan']:
            if 'tcp' in scan_result['scan'][host]:
                portresults = scan_result['scan'][host]['tcp']
                for service in portresults:
                    print bcolors.OKGREEN + 'Found open port: ' + str(service) + ' (' + ports.get(ports.port == service).description + ')' + bcolors.ENDC
                    host_id = host_current.get(host_current.hostIP == host).id
                    services.create(hostID=host_id, portID=service, scanTime=timestamp)

    def os_fingerprint(self):
        IPChecks = network()
        query = host_current.select(fn.Max(host_current.scanTime).alias('count'))
        for i in query:
            timestamp = i.count
        for i in host_current.select(host_current.hostIP, host_current.hostname).where(host_current.scanTime == timestamp):
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
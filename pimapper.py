#!/usr/bin/python

import time
import nmap
import sys
import netaddr
from netaddr import IPNetwork, IPAddress
import includes.settings
import includes.database
from includes.settings import bcolors
from includes.database import *
from includes.network import network
import commands
import time

primaryIf='eth0'

IPChecks = network()

currentIP = commands.getoutput("/sbin/ifconfig").split("\n")[1].split()[1][5:]
currentCIDR = IPChecks.getBits(IPChecks.get_netmask(primaryIf))
currentPreRange = currentIP + "/" + str(currentCIDR)
ip2 = IPNetwork(currentPreRange)
currentRange = str(ip2.network) + "/" + str(currentCIDR)

timestamp = int(time.time())

nm = nmap.PortScannerAsync()

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


def callback_result(host, scan_result):
	addHost = True
	addMac = True
	try:
		scan_result['scan'][host]['status']['state'] == 'up'
	except:
		pass
	else:	
		hostnameNice=scan_result['scan'][host]['hostname']
		try:
			host_current.get(host_current.hostname == hostnameNice)
			for i in host_current.select().where(host_current.hostname == hostnameNice):
				if i.hostIP != host:
					hostUpdate = host_current.update(hostIP=host).where(host_current.hostname == hostnameNice)
					hostUpdate.execute()
					print bcolors.OKBLUE + 'Existing Host Updated' + bcolors.ENDC + '( ' + hostnameNice + ' - ' + host + ' )'
				else:
					print bcolors.OKGREEN + 'Existing Host Found' + bcolors.ENDC + '( ' + hostnameNice + ' - ' + host + ' )'
		except:
                	host_current.create(
				hostname=hostnameNice,
                      		hostIP=host,
                       		scanTime=timestamp,
                     	)
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

nm.scan(hosts=scanRange, arguments='-sP', callback=callback_result)

while nm.still_scanning():
	time.sleep(0.1)
	sys.stdout.write("-")
	sys.stdout.flush()
print bcolors.HEADER + '\nScan complete' + bcolors.ENDC


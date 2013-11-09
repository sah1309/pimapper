#!/usr/bin/python

import time
import nmap
import sys
import netaddr
import includes.settings
import includes.database
from includes.settings import bcolors
from includes.database import *
from includes.network import network
import commands
import time

currentIP = commands.getoutput("/sbin/ifconfig").split("\n")[1].split()[1][5:]
timestamp = int(time.time())

try:
	host_current.create_table()
except:
	pass

nm = nmap.PortScannerAsync()

IPChecks = network()
scanRange = raw_input('Please enter your scan range in CIDR format: ')
if IPChecks.subnetCheck(currentIP, scanRange) == False:
	print ' This subnet is outside your own, MAC Address gathering is disabled'
	macDisable = True

def callback_result(host, scan_result):
	try:
		scan_result['scan'][host]['status']['state'] == 'up'
	except:
		pass
	else:
		try:
			host_current.get(host_current.hostname == scan_result['scan'][host]['hostname'])
			hostCheck = host_current.select().where(host_current.hostname == scan_result['scan'][host]['hostname']).order_by(host_current.scanTime.desc()).limit(1)
			for i in hostCheck:
				if i.hostIP != host:
					hostUpdate = host_current.update(hostIP=host).where(host_current.hostname == scan_result['scan'][host]['hostname'])
					hostUpdate.execute()
					print bcolors.OKBLUE + 'Existing Host Updated' + bcolors.ENDC + '(' + host + ')'
				else:
					print bcolors.OKGREEN + 'Existing Host Found' + bcolors.ENDC + '(' + host + ' - ' + IPChecks.getMac(host) + ')'
		except:		
			host_current.create(
				hostname=scan_result['scan'][host]['hostname'],
				hostIP=host,
				scanTime=timestamp,
			)
			print bcolors.WARNING + 'New Host Found' + bcolors.ENDC + '(' + host + ')'


nm.scan(hosts=scanRange, arguments='-sP', callback=callback_result)

print bcolors.HEADER + 'Starting pimapper discovery scan' + bcolors.ENDC
while nm.still_scanning():
	time.sleep(0.1)
	sys.stdout.write("-")
	sys.stdout.flush()
print bcolors.HEADER + '\nScan complete' + bcolors.ENDC


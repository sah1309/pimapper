#!/usr/bin/python

#import libraries
import nmap
import time
import sys
import peewee
from includes.settings import bcolors



nm = nmap.PortScannerAsync()

def callback_result(host, scan_result):
	try:
		scan_result['scan'][host]['status']['state'] == 'up'
	except:
		pass
	else:
	#	print host, scan_result
		print bcolors.OKGREEN + 'Host Found' + bcolors.ENDC + '(' + host + ')'

nm.scan(hosts='172.16.10.0/24', arguments='-sP', callback=callback_result)

print bcolors.HEADER + 'Starting pimapper discovery scan' + bcolors.ENDC
while nm.still_scanning():
	time.sleep(0.1)
	sys.stdout.write("-")
	sys.stdout.flush()
print bcolors.HEADER + '\nScan complete' + bcolors.ENDC


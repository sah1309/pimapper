#!/usr/bin/python

from netaddr import IPNetwork, IPAddress
import subprocess
import re

class network():
	def subnetCheck(self, ip, cidr):
		if IPAddress(ip) in IPNetwork(cidr):
    			return True
		else:
			return False

	def getMac(self, host):
		cmd = 'arping -c 1 ' + host
		p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
		output, errors = p.communicate()
		if output is not None :
			mac = re.search(r'([0-9A-F]{2}[:-]){5}([0-9A-F]{2})', output, re.I).group()
			return mac

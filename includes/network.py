#!/usr/bin/python

from netaddr import IPNetwork, IPAddress
import subprocess
import re
import socket
import fcntl
import struct
import sys

class network():
	def subnetCheck(self, ip, cidr):
		if IPAddress(ip) in IPNetwork(cidr):
    			return True
		else:
			return False

	def getMac(self, host):
		cmd = 'arping -c 2 ' + host
		p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
		output, errors = p.communicate()
		if output is not None :
			mac = re.search(r'([0-9A-F]{2}[:-]){5}([0-9A-F]{2})', output, re.I)
			if mac:
				return mac.group()

	def getBits(self, netmask):
		mask = IPAddress(netmask)
		return mask.bits().count('1')

	def get_netmask(self, ifname):
        	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        	return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x891b, struct.pack('256s',ifname))[20:24])

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


        def os_match(self, host, option):

            try:
                    if option == 'lan':
                            scanv = subprocess.Popen(["nmap", "--osscan-guess", "-PR", "-O", str(host)],stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
                    else:
                            scanv = subprocess.Popen(["nmap", "-PE","-PP","-PS21,22,23,25,80,443,3306,3389,8080","-O", str(host)],stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
            except OSError:
                print "Install nmap: sudo apt-get install nmap"
		
            scanlist=scanv.split()

            if 'printer' in scanlist:
                    osmatch = 'Printer'
            elif 'Fortinet' in scanlist:
                    osmatch = 'Fortinet'
            elif 'Linux' in scanlist:
                    osmatch = 'Linux'
            elif 'Windows' in scanlist:
                    osmatch = 'Windows'
            elif 'Apple' in scanlist:
                    osmatch = 'Apple'
            elif 'IOS' in scanlist:
                    osmatch = 'IOS'
            else:
                    osmatch = 'Unknown'

            percent = [s for s in scanlist if s.endswith('%),')]

            if not percent:
                percent = '0%'

            return osmatch, percent[0].strip('%(),')

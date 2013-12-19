#!/usr/bin/python

from netaddr import IPNetwork, IPAddress
import subprocess, re, socket, fcntl, struct, sys

class network():

        # Check to see if IP address (ip) is contained in IP range (cidr)
        def subnetCheck(self, ip, cidr):
                if IPAddress(ip) in IPNetwork(cidr):
                        return True
                else:
                        return False
        # Get mac address for IP address (host)
        def getMac(self, host):
                cmd = 'arping -c 2 ' + host
                p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
                output, errors = p.communicate()
                if output is not None :
                        mac = re.search(r'([0-9A-F]{2}[:-]){5}([0-9A-F]{2})', output, re.I)
                        if mac:
                                return mac.group()

        # Get slash notation from subnet mask to build CIDR notations
        def getBits(self, netmask):
                mask = IPAddress(netmask)
                return mask.bits().count('1')

        # Get subnet mask of current interface connection
        def get_netmask(self, ifname):
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x891b, struct.pack('256s',ifname))[20:24])

        # Uses Nmap to detect Operating system of host - if option set to 'lan' then run more intensive scan
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
            if 'Cisco' in scanlist:
                    osmatch = 'Cisco'
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

import peewee
from peewee import *

db = MySQLDatabase('pimapper', user='root',passwd='pa55word')

def write_mac_db(mac, datetime):
    from settings import bcolors
    current.create(
        macAddress=mac,
        scanTime=datetime,
    )
    print bcolors.OKGREEN + 'MAC address stored ' + bcolors.ENDC + '( ' + mac + ' )'

def write_hostip_db(mac, ip):
    from settings import bcolors
    hostid = current.get(current.macAddress == mac)
    for address in ipaddress.select():
        if address.ipaddress == ip and address.id == hostid.id:
            return False
        else:
            ipaddress.create(
                hostid=hostid.id,
                ipaddress=ip,
            )
            print bcolors.OKGREEN + 'IP address stored for host:' + str(hostid.id) + bcolors.ENDC
            return True

class current(peewee.Model):
    id = peewee.IntegerField()
    macAddress = peewee.CharField()
    scanTime = peewee.DateTimeField()

    class Meta:
        database = db

class ipaddress(peewee.Model):
    id = peewee.IntegerField()
    hostid = peewee.IntegerField()
    ipaddress = peewee.CharField()

    class Meta:
        database = db

try:
    current.create_table()
except:
    pass

try:
    ipaddress.create_table()
except:
    pass

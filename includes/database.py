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


class current(peewee.Model):
    id = peewee.IntegerField()
    macAddress = peewee.CharField()
    scanTime = peewee.DateTimeField()

    class Meta:
        database = db

class ipaddress(peewee.Model):
    id = peewee.IntegerField()
    ipaddress = peewee.IntegerField()

    class Meta:
        database = db

try:
        current.create_table()
except:
        pass

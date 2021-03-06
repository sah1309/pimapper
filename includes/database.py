
# Database setup file

import logging, peewee
logging.basicConfig()
from peewee import *

db = MySQLDatabase('pimapper', user='root',passwd='pa55word')

class os_match(peewee.Model):
    hostID = peewee.IntegerField()
    os = peewee.CharField()
    confidence = peewee.IntegerField()
    scanTime = peewee.IntegerField()

    class Meta:
        database = db

class services(peewee.Model):
    hostID = peewee.IntegerField()
    portID = peewee.IntegerField()
    scanTime = peewee.CharField()

    class Meta:
        database = db

class ports(peewee.Model):
    service = peewee.CharField()
    port = peewee.CharField()
    protocol = peewee.CharField()
    description = peewee.CharField()

    class Meta:
        database = db

class mac_address(peewee.Model):
    hostname = peewee.CharField()
    macAddr = peewee.CharField()
    scanTime = peewee.CharField()

    class Meta:
        database = db

class host_current(peewee.Model):
    hostname = peewee.CharField()
    hostIP = peewee.CharField()
    scanTime = peewee.CharField()

    class Meta:
        database = db

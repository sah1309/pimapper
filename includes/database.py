import peewee
from peewee import *

db = MySQLDatabase('pimapper', user='root',passwd='pa55word')

class host_current(peewee.Model):
    hostname = peewee.CharField()
    hostIP = peewee.CharField()
    scanTime = peewee.CharField()

    class Meta:
        database = db

class host_history(peewee.Model):
    hostname = peewee.CharField()
    hostIP = peewee.CharField()
    scanTime = peewee.CharField()

    class Meta:
        database = db

class mac(peewee.Model):
    hostname = peewee.CharField()
    macAddr = peewee.CharField()
    scanTime = peewee.CharField()

    class Meta:
        database = db

try:
        host_current.create_table()
except:
        pass
try:
        host_history.create_table()
except:
        pass
try:
        mac.create_table()
except:
        pass

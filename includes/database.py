import peewee
from peewee import Model, MySQLDatabase

db = MySQLDatabase('pimapper', user='root',passwd='pa55word')

class ports(peewee.Model):
    service = peewee.CharField()
    port = peewee.CharField()
    protocol = peewee.CharField()
    description = peewee.CharField()

    class Meta:
        database = db

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

class live_ip(peewee.Model):
    ipaddress = peewee.CharField()
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
        live_ip.create_table()
except:
        pass
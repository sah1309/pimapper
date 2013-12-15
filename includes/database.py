import peewee
from peewee import Model, MySQLDatabase

db = MySQLDatabase('pimapper', user='root',passwd='pa55word')

class os_match(peewee.Model):
    hostID = peewee.IntegerField()
    os = peewee.CharField()
    confidence = peewee.IntegerField()
    scanTime = peewee.IntegerField()

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

class host_history(peewee.Model):
    hostname = peewee.CharField()
    hostIP = peewee.CharField()
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
        mac_address.create_table()
except:
        pass
try:
        services.create_table()
except:
        pass
try:
        os_match.create_table()
except:
        pass
#!/usr/bin/python

#import libraries
import nmap
import time
import sys
import peewee
from peewee import *
from includes.settings import bcolors

timestamp = int(time.time())
db = MySQLDatabase('pimapper', user='root',passwd='pa55word')


class host_current(peewee.Model):
    hostname = peewee.CharField()
    hostIP = peewee.CharField()
    scanTime = peewee.CharField()

    class Meta:
        database = db


host = '172.16.10.1'
hostname1= 'SkyRouter.home'

hostCheck = host_current.select().where(host_current.hostname == hostname1).order_by(host_current.scanTime.desc()).limit(1)
for i in hostCheck:
	if i.hostIP == host:
		host_current.update(hostIP=host).where(host_current.host == hostname1)

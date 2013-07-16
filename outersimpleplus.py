#!/usr/bin/python

import MySQLdb
import subprocess
from time import sleep
from ConfigParser import SafeConfigParser

parser = SafeConfigParser()
parser.read('../settings.conf')

dbhost=parser.get('DB', 'hostname')
dbuser=parser.get('DB', 'username')
dbpassword=parser.get('DB', 'password')
dbdb=parser.get('DB', 'dbname')

db=MySQLdb.connect(dbhost,dbuser,dbpassword,dbdb)
cursor=db.cursor(MySQLdb.cursors.DictCursor)

cursor.execute("select eid, URL from searchresults where URL like 'https://plus.google.com%' order by lastcrawl desc")

sqlkeyword=cursor.fetchall()

for data in sqlkeyword:
	eid=str(data['eid'])
	url=str(data['URL'])
	print '*** STARTING TO SCRAPE *** '+url
	subprocess.check_output(['scrapy','crawl','simpleplusspider','-a','source='+url])
	sleep(10);

print "Outer run completed"

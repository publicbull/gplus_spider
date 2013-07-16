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

cursor.execute("select eid, URL, Lastcrawl from searchresults where URL like 'https://plus.google.com%' and (now() > DATE_ADD(Lastcrawl,INTERVAL 7 DAY) or Lastcrawl is null) order by lastcrawl desc")
#cursor.execute("select eid, URL, Lastcrawl from searchresults where URL like 'https://plus.google.com%'")

sqlkeyword=cursor.fetchall()

print sqlkeyword

for data in sqlkeyword:
	eid=str(data['eid'])
	url=str(data['URL'])
	print '*** STARTING TO SCRAPE *** '+url
	scrapy_run='scrapy crawl pspider -a source='+url+' -a eid='+eid
	subprocess.check_output(['scrapy','crawl','pspider','-a','source='+url,'-a','eid='+eid])
	sleep(10);

print "Outer run completed"

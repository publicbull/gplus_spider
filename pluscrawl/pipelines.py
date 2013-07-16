# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

from pluscrawl.settings import *

class PluscrawlPipeline(object):
    def process_item(self, item, spider):
        URL=str(item['URL'])
        author=str(item['author'])
        author_url=str(item['author_url'])
        review_date=str(item['review_date'])
        review_rate=str(item['review_rate'])
        review_text=str(item['review_text'])
        eid=int(item['eid'])
        query="""INSERT INTO placesresults (URL,author,author_url,review_text,text_rating,eid,review_date) VALUES ('%s','%s','%s','%s','%s','%s',date_sub(date(now()),interval %s))"""%(URL,author,author_url,review_text,review_rate,eid,review_date)
        cursor.execute(query)
        db.commit()

        return item

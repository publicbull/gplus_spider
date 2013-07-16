# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class PluscrawlItem(Item):
    # define the fields for your item here like:
    # name = Field()
    URL=Field()
    author=Field()
    author_url=Field()
    review_date=Field()
    review_text=Field()
    review_rate=Field()
    eid=Field()
    pass

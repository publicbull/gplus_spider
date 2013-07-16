from scrapy.spider import BaseSpider
from scrapy.http import FormRequest
from scrapy.selector import HtmlXPathSelector
from scrapy.shell import inspect_response
from scrapy.http import Request
from time import sleep
import re
from pluscrawl.items import *
from pluscrawl.settings import *

class LoginSpider(BaseSpider):
    page_incr=0    
    rank=0
    end_flag=0

    name = 'simpleplusspider'
    start_urls = ['http://plus.google.com']

    def __init__(self,source=""):
        self.start_urls = [source]
        self.URL=source


    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        results = hxs.select('//div[@class="Hwa"]/div/div')
        
        for res in results:    
            author = res.select('div/div[2]/span[1]/a/text()').extract()
            
            if author:
                author=author[0]
            else:
                author='Null'
            author_url=res.select("div/div[2]/span[1]/a/@href").extract()
            
            if author_url:
                author_url="https://plus.google.com"+str(author_url[0])[1:]
            else:
                author_url='Null'
            
            review_date=res.select('div/div[2]/span[2]/text()').extract()
            review_rate=res.select('div/div[2]/div/span/span[2]/text()').extract()
            review_rate=review_rate[0]
            review_text=res.select('div/div[2]/div[2]/span/text()').extract()
            
            if review_text:
                review_text=review_text[0]
            else:
                review_text='Null'
            
            prop = PluscrawlItem(
                author = author,
                URL=self.URL,
                author_url = author_url,
                review_date = review_date,
                review_rate = review_rate,
                review_text=review_text
            )
            yield prop
           


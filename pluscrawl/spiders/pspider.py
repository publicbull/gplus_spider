from scrapy.spider import BaseSpider
from scrapy.http import FormRequest
from scrapy.selector import HtmlXPathSelector
from scrapy.shell import inspect_response
from scrapy.http import Request
from time import sleep
import re
from pluscrawl.items import *
from pluscrawl.settings import *
from selenium import webdriver

class LoginSpider(BaseSpider):
    page_incr=0    
    rank=0
    end_flag=0

    name = 'pspider'
    start_urls = ['https://plus.google.com']

    def __init__(self,source="https://plus.google.com/111426342394540331997/about",eid="0"):
        self.start_urls = [source]
        self.URL=source+"?hl=en"
        self.eid=eid

    def parse(self, response):
        print self.URL," ",self.eid
        print "starting phantomjs"
        #dr=webdriver.PhantomJS('/home/ubuntu/phantomjs/bin/phantomjs')

        dr=webdriver.PhantomJS('/home/jezeel/Desktop/phantomjs/bin/phantomjs')  
 
        dr.get(self.URL)        
        while(True):
            try:
                dr.find_element_by_xpath("//span[@class='a-n Op Ht']").click()
                sleep(10)
            except:
                break

        sou=dr.page_source
        sou2=sou.encode('ascii','ignore')

        hxs = HtmlXPathSelector(text=sou2)
        results=hxs.select('//div[@class="Hwa"]//div[@role="article"]')
        #print results,len(results)        
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
            
            review_date=res.select('div/div[@class="Uya"]/div[1]/div[2]/span/text()').extract()

            if review_date:
                review_date=review_date[0]
                review_date=review_date[9:review_date.find(" ago")]


                def date_format(date_rev):
                    if 'day' in date_rev:
                        dt=date_rev[0:date_rev.find(" ")]
                        if dt=='a':
                            dt=1
                        date_rev=str(dt)+" day"
                        return date_rev
                    elif 'week' in date_rev:
                        dt=date_rev[0:date_rev.find(" ")]
                        if dt=='a':
                            dt=1
                        date_rev=str(dt)+" week"
                        return date_rev
                    elif 'month' in date_rev:
                        dt=date_rev[0:date_rev.find(" ")]
                        if dt=='a':
                            dt=1
                        date_rev=str(dt)+" month"
                        return date_rev
                    elif 'year' in date_rev:
                        dt=date_rev[0:date_rev.find(" ")]
                        if dt=='a':
                            dt=1
                        date_rev=str(dt)+" year"
                        return date_rev            

                review_date=date_format(review_date)
            
            review_rate=res.select('div/div[2]/div/span/span[2]/text()').extract()
            if review_rate:
                review_rate=review_rate[0]
            else:
                review_rate='Null'

            review_text=res.select('div/div[2]/div[2]/span/text()').extract()
            if review_text:
                review_text=review_text[0]
                review_text=review_text.replace("'","")
                review_text=review_text.replace("\"","")
            else:
                review_text='Null'
            
            prop = PluscrawlItem(
                URL=self.URL,
                author = author,
                author_url = author_url,
                review_date = review_date,
                review_rate = review_rate,
                review_text=review_text,
                eid=self.eid
            )
            print prop
            
            yield prop

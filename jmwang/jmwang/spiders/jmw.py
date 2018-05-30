# -*- coding: utf-8 -*-
import scrapy
from jmwang.items import  JmwangItem


class JmwSpider(scrapy.Spider):
    name = 'jmw'
    allowed_domains = ['jmw.com.cn']
    start_urls = ['http://jmw.com.cn/']

    def parse(self, response):
        pass

    def start_requests(self):
        urls = []
        for pid in range(0, 878):
            urls.append("http://www.jmw.com.cn/category/canyin/"+str(pid)+".html")
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        item = JmwangItem()
        body=response.body
        brands =body.xpath("//.div_listeach")
        item['brands'] = brand["title"]
        item['url'] = response.url
        print(item['brands'])
        print(item['url'])
        yield item


# -*- coding: utf-8 -*-
import scrapy
from u88link.items import U88LinkItem
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
class U88sipderSpider(scrapy.Spider):
    name = 'u88sipder'
    allowed_domains = ['www.phone.net']
    start_urls = ['http://www.phone.net/']
    def parse(self, response):
        item = U88LinkItem()
        sel = scrapy.Selector(response)
        print(response.url,response.status)
        links_in_a_page = sel.xpath('//a[@href]')  # 页面内的所有链接
        for link_sel in links_in_a_page:
            link = str(link_sel.re('href="(.*?)"')[0]) # 每一个url
            link=link.replace('%20', '')
            if link is not None:
                yield scrapy.Request(response.urljoin(link.rstrip()), callback=self.parse,
                                     errback=self.errback_httpbin,meta={'dont_redirect': True})
                #link_text = link_sel.xpath('text()').extract()  # 每个url的链接文本, 若不存在设为None
                #if link_text:
                 #   item['title'] = str(link_text[0].strip())
                #else:
                #    item['title'] = None
                #item['status'] = response.status
                #item['link']=response.urljoin(link)

                #yield item

    def parse_httpbin(self, response):
        self.logger.info('Got successful response from {}'.format(response.url))
        # do something useful here...

    def errback_httpbin(self, failure):
        item = U88LinkItem()
        # log all failures
        #self.logger.error(repr(failure))
        # in case you want to do something special for some errors,
        # you may need the failure's type:
        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            referers = response.request.headers.get('Referer',None)
            item['link']=response.url
            item['status']=response.status
            item['referer']=referers
            print(response.url,response.status,referers)
            yield scrapy.Request(response.url, callback=self.parse,
                                 errback=self.errback_httpbin)
            yield item
            #self.logger.error('HttpError on %d,%s', (response.url,response.status))
        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)
        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)

# -*- coding: utf-8 -*-
from scrapy.downloadermiddlewares.redirect import RedirectMiddleware
from u88link.items import U88LinkItem
class RedirectUrlMiddleware(RedirectMiddleware):
    def process_response(self, request, response, spider):
        url = response.url
        #exit(2000)
        if response.status in [301, 302]:
            #log.msg("trying to redirect us: %s" % url, level=log.INFO)
            print(response.url)
            print(response.status)
            item = U88LinkItem()
            item['link'] = response.url;
            item['status'] = response.url;
            #yield item
        return request
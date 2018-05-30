# -*- coding: utf-8 -*-
from scrapy.downloadermiddlewares.redirect import RedirectMiddleware
from scrapy import log
from u88link.items import U88LinkItem
class RedirectUrlMiddleware(RedirectMiddleware):
    def process_response(self, request, response, spider):
        url = response.url
        #log.msg("trying to redirect us: %s%d" % url, level=log.INFO)
        if response.status in [301, 302,404]:
            log.msg("trying to redirect us: %s" % url, level=log.INFO)
            print(response.url)
            print(response.status)
            item = U88LinkItem()
            item['link'] = response.url;
            item['status'] = response.url;
            #yield item
        return response
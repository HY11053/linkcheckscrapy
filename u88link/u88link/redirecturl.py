# -*- coding: utf-8 -*-
from scrapy.downloadermiddlewares.redirect import RedirectMiddleware
from scrapy import log
class RedirectUrlMiddleware(RedirectMiddleware):
    def process_response(self, request, response, spider):
        url = response.url
        #log.msg("trying to redirect us: %s%d" % url, level=log.INFO)
        if response.status in [301, 302]:
            log.msg("trying to redirect us: %d" % response.status, level=log.INFO)
            print(response.url)
            print(response.status)
            #yield item
        return response
# -*- coding: utf-8 -*-
import time
from random import choice

import scrapy

from Hotspot.items import BaiduItem
from Hotspot.static import Source
from utils.spider_headers import USER_AGENT_LIST
from utils.tools import get_md5


class BaiduHotspotSpider(scrapy.Spider):
    name = 'baidu'
    allowed_domains = ['top.baidu.com/buzz?b=1&fr=topindex']
    headers = {
        'User-Agent': choice(USER_AGENT_LIST)
    }
    start_urls = ['http://top.baidu.com/buzz?b=1&fr=topindex/']

    def parse(self, response):
        node_list = response.xpath(".//tr[not(@class='item-tr')][position()>1]")
        for node in node_list:
            item = BaiduItem()
            item['title'] = node.xpath(".//a[@class='list-title']/text()").get().strip()
            item['link'] = node.xpath(".//a[@class='list-title']/@href").get().strip()
            item['value'] = node.xpath(".//td[@class='last']/span/text()").get().strip()
            item['timestamp'] = int(time.time() * 1000)
            item['title_md5'] = get_md5(item['title'])
            item['source'] = Source.BAIDU.value
            yield item

    def close(spider, reason):
        print('+' * 50, '爬虫结束了')

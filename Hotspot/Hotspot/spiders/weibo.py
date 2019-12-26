# -*- coding: utf-8 -*-
import time
from random import choice

import scrapy

from Hotspot.items import WeiboItem
from Hotspot.static import Source
from utils.spider_headers import USER_AGENT_LIST
from utils.tools import get_md5


class BaiduHotspotSpider(scrapy.Spider):
    name = 'weibo'
    allowed_domains = ['s.weibo.com/top/summary']
    headers = {
        'User-Agent': choice(USER_AGENT_LIST)
    }
    start_urls = ['https://s.weibo.com/top/summary']
    base_url = 'https://s.weibo.com'

    def parse(self, response):
        node_list = response.xpath(".//div[@class='data']//tr[position()>1]")
        print('-' * 50, len(node_list))
        for node in node_list:
            item = WeiboItem()
            item['title'] = node.xpath(".//td[@class='td-02']/a/text()").extract_first().strip()
            item['value'] = node.xpath(".//td[@class='td-02']/span/text()").extract_first().strip()
            item['timestamp'] = int(time.time() * 1000)
            item['title_md5'] = get_md5(item['title'])
            item['source'] = Source.WEIBO.value

            link_href_to = node.xpath(".//td[@class='td-02']/a/@href_to").extract_first()

            if link_href_to:
                item['link'] = self.base_url + link_href_to.strip()
            else:
                item['link'] = self.base_url + node.xpath(".//td[@class='td-02']/a/@href").extract_first().strip()

            yield item

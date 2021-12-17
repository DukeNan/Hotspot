# -*- coding: utf-8 -*-
import json
import re
import time
from random import choice

import scrapy

from Hotspot.items import BaiduItem
from Hotspot.static import Source
from utils.spider_headers import USER_AGENT_LIST
from utils.tools import get_md5


class BaiduHotspotSpider(scrapy.Spider):
    name = 'baidu'
    allowed_domains = ['top.baidu.com/board?tab=realtime']
    headers = {
        'User-Agent': choice(USER_AGENT_LIST)
    }
    start_urls = ['https://top.baidu.com/board?tab=realtime']

    def parse(self, response):
        data_list = self.get_data_list(response.text)
        for temp in data_list:
            item = BaiduItem()
            item['title'] = temp.get('word', '').strip('#')
            item['link'] = temp.get('rawUrl')
            item['value'] = temp.get('hotScore')
            item['timestamp'] = int(time.time() * 1000)
            item['title_md5'] = get_md5(item['title'])
            item['source'] = Source.BAIDU.value
            yield item

    def get_data_list(self, str_data):
        results = re.findall(r'<!--s-data:(.+?)-->', str_data)
        if not results:
            return None
        data_dict = json.loads(results[0])
        return data_dict['data']['cards'][0]['content']

    def close(spider, reason):
        pass

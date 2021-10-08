# -*- coding: utf-8 -*-
import json
import re
import time
from random import choice
from urllib.parse import urlencode

import scrapy

from Hotspot.items import WeiboItem
from Hotspot.static import Source
from utils.spider_headers import USER_AGENT_LIST
from utils.tools import get_md5


class WeiBoHotspotSpider(scrapy.Spider):
    name = 'weibo'
    url = 'https://s.weibo.com/top/summary'
    base_url = 'https://s.weibo.com'

    def start_requests(self):
        url = 'https://passport.weibo.com/visitor/genvisitor'
        data = {
            'cb': 'gen_callback'
        }
        yield scrapy.FormRequest(url=url, formdata=data, method='post', callback=self.get_sub_data)

    def get_sub_data(self, response):
        url = 'https://passport.weibo.com/visitor/visitor?'
        params = {
            'a': 'incarnate',
            't': self.get_tid_str(response.text),
            'w': 3,
            'c': 100,
            'cb': 'cross_domain',
            'from': 'weibo',
        }
        url = url + urlencode(params)
        yield scrapy.Request(url=url, callback=self.get_weibo_top_summary)

    def get_weibo_top_summary(self, response):

        sub_dict = self.get_sub_dict(response.text)
        sub = sub_dict.get('sub')
        subp = sub_dict.get('subp')
        headers = {
            'User-Agent': choice(USER_AGENT_LIST),
            'Cookie': f"SUB={sub}; SUBP={subp}"
        }
        yield scrapy.Request(url=self.url, headers=headers, callback=self.parse)

    def parse(self, response):
        node_list = response.xpath(".//div[@class='data']//tr[position()>1]")
        print('-' * 50, len(node_list))
        for node in node_list:
            value_str = node.xpath(".//td[@class='td-02']/span/text()").extract_first().strip()
            if not value_str:
                continue
            item = WeiboItem()
            item['title'] = node.xpath(".//td[@class='td-02']/a/text()").extract_first().strip()
            item['value'] = re.findall(r"\d+", value_str)[0]
            item['timestamp'] = int(time.time() * 1000)
            item['title_md5'] = get_md5(item['title'])
            item['source'] = Source.WEIBO.value

            link_href_to = node.xpath(".//td[@class='td-02']/a/@href_to").extract_first()

            if link_href_to:
                item['link'] = self.base_url + link_href_to.strip()
            else:
                item['link'] = self.base_url + node.xpath(".//td[@class='td-02']/a/@href").extract_first().strip()

            yield item

    def get_tid_str(self, str_data):
        results = re.findall(r'gen_callback\((.+?)\);', str_data)
        if results:
            json_data = results[0]
            data_dict = json.loads(json_data)
            return data_dict['data']['tid']
        return None

    def get_sub_dict(self, str_data):
        results = re.findall(r'cross_domain\((.+?)\);', str_data)
        if results:
            json_data = results[0]
            data_dict = json.loads(json_data)
            return data_dict['data']
        return {}

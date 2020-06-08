# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy import func, text

from Hotspot.items import BaiduItem, WeiboItem
from dao import engine
from dao.iinflux import client
from dao.models import BaiduHot, WeiboHot


class HotspotPipeline(object):

    def __init__(self):
        self.baidu = dict()
        self.weibo = dict()

    def process_item(self, item, spider):
        if isinstance(item, BaiduItem):
            stmt = text('replace into baidu_hot set title=:title, `value`=:value, title_md5=:title_md5, \
                        `timestamp`=:timestamp, link=:link, `source`=:source')
        else:
            stmt = text('replace into weibo_hot set title=:title, `value`=:value, title_md5=:title_md5, \
                                    `timestamp`=:timestamp, link=:link, `source`=:source')
        with engine.connect() as conn:
            conn.execute(stmt, **item)

        return item


class InfluxPipeline:
    def __init__(self):
        self.json_body = []
        self.influx_client = client

    def process_item(self, item, spider):
        measurement = None
        if isinstance(item, BaiduItem):
            measurement = 'baidu'
        elif isinstance(item, WeiboItem):
            measurement = 'weibo'
        temp = {
            'measurement': measurement,
            'tags': {
                'title_md5': item['title_md5'],
                'title': item['title'],
            },
            'fields': {

                'value': float(item['value']),
            }
        }
        self.json_body.append(temp)

        return item

    def close_spider(self, spider):
        self.influx_client.write_points(self.json_body)
        self.influx_client.close()

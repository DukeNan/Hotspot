# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy import func

from Hotspot.items import BaiduItem, WeiboItem
from dao import session
from dao.iinflux import client
from dao.models import BaiduHot, WeiboHot


class HotspotPipeline(object):

    def __init__(self):
        self.conn = session
        self.baidu = dict()
        self.weibo = dict()

    def process_item(self, item, spider):
        if isinstance(item, BaiduItem):
            Model = BaiduHot
        else:
            Model = WeiboHot
        today_data = self.today_data(Model)
        yesterday_data = self.yesterday_data(Model)
        post_data = dict(item)
        if item['title_md5'] in today_data:
            return item
        post_data['number'] = yesterday_data.get(item['title_md5'], 0) + 1
        instance = Model(**post_data)
        self.conn.add(instance)

        return item

    def close_spider(self, spider):
        self.conn.commit()
        self.conn.close()

    def today_data(self, Model) -> set:
        """return title_md5 set"""
        queryset = self.conn.query(Model.title_md5).filter(func.date(Model.create_time) == func.current_date()).all()
        return {query.title_md5 for query in queryset}

    def yesterday_data(self, Model) -> dict:
        queryset = self.conn.query(Model.title_md5, Model.number). \
            filter(func.datediff(func.current_timestamp(), Model.create_time) == 1).all()
        return {query.title_md5: query.number for query in queryset}


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

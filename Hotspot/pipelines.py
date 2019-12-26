# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from dao import session
from dao.models import BaiduHot, WeiboHot
from Hotspot.items import BaiduItem, WeiboItem
from sqlalchemy import func
from influxdb import InfluxDBClient
from scrapy.utils.project import get_project_settings


class HotspotPipeline(object):

    def __init__(self):
        self.conn = session

    def process_item(self, item, spider):
        if isinstance(item, BaiduItem):
            if self.conn.query(BaiduHot).filter(BaiduHot.title_md5 == item['title_md5'],
                                                func.date(BaiduHot.create_time) == func.current_date()).first():
                return item
            baidu_hot = BaiduHot(**dict(item))
            self.conn.add(baidu_hot)
        if isinstance(item, WeiboItem):
            if self.conn.query(WeiboHot).filter(WeiboHot.title_md5 == item['title_md5'],
                                                func.date(WeiboHot.create_time) == func.current_date()).first():
                return item
            weibo_hot = WeiboHot(**dict(item))
            self.conn.add(weibo_hot)

        return item

    def close_spider(self, spider):
        self.conn.commit()
        self.conn.close()


class InfluxPipeline:
    def __init__(self):
        self.json_body = []
        self.settings = get_project_settings()
        self.influx_client = InfluxDBClient(
            host=self.settings['INFLUX_DB_HOST'],
            port=self.settings['INFLUX_DB_PORT'],
            username=self.settings['INFLUX_DB_USERNAME'],
            password=self.settings['INFLUX_DB_PASSWORD'],
            database=self.settings['INFLUX_DB_NAME']
        )

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
            },
            'fields': {
                'title': item['title'],
                'value': item['value'],
                # 'value': 111111
            }
        }
        self.json_body.append(temp)


        return item

    def close_spider(self, spider):
        self.influx_client.write_points(self.json_body)
        self.influx_client.close()

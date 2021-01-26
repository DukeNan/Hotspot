# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy import text

from Hotspot.items import BaiduItem, WeiboItem
from dao import session, engine
from dao.models import PushMessage
from dao.iinflux import client
from Hotspot.settings import WxPusherConfig
import requests


class HotspotPipeline(object):

    def __init__(self):
        self.baidu = dict()
        self.weibo = dict()

    def process_item(self, item, spider):
        if isinstance(item, BaiduItem):
            table_name = 'baidu_hot'
        elif isinstance(item, WeiboItem):
            table_name = 'weibo_hot'
        else:
            raise ValueError('数据格式错误')

        sql = f"""insert into {table_name}(title, value, title_md5, timestamp, link) \
                  select :title, :value, :title_md5, :timestamp, :link from dual \
                  where not exists(select id from {table_name} where title_md5=:title_md5)"""
        with engine.connect() as conn:
            conn.execute(text(sql), **item)

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


class MessagePushPipeline(object):
    def __init__(self):
        self.data_list = []
        self.db_session = session

    def push_message2wx(self, data_list):
        index_data = data_list[0]
        if self.db_session.query(PushMessage).filter_by(hash_code=index_data['title_md5']).first():
            return
        # 推送微信消息
        content = '今日微博💥🍉：'
        if len(data_list) > 1:

            for index, data in enumerate(data_list[:5]):
                content += '\n{0}.{1}'.format(index + 1, data['title'])
        else:
            content += '\n热搜：{}'.format(data_list[0]['title'])
        data = {
            "appToken": WxPusherConfig['appToken'],
            "content": content,
            "contentType": 1,
            "topicIds": WxPusherConfig['topicIds'],

            "url": "https://s.weibo.com/top/summary"
        }
        resp = requests.post(WxPusherConfig['post_url'], json=data).json()
        self.db_session.add(PushMessage(summary=index_data['title'],
                                        hash_code=index_data['title_md5'],
                                        code=resp['code'],
                                        push_type='weibo',
                                        body=data,
                                        response=resp))
        self.db_session.commit()

    def process_item(self, item, spider):
        if isinstance(item, WeiboItem):
            # 热度值
            hot_value = int(item['value'])
            #  大于5百万热值
            if hot_value > 500000:
                self.data_list.append(dict(item, value=hot_value))
        return item

    def close_spider(self, spider):
        if not self.data_list:
            return
        data_list = sorted(self.data_list, key=lambda x: x['value'], reverse=True)
        self.push_message2wx(data_list)
        self.db_session.close()

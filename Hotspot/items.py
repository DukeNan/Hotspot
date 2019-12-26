# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BaiduItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 标题
    title = scrapy.Field()
    # 热搜值
    value = scrapy.Field()
    # 链接地址
    link = scrapy.Field()
    # 创建时间13位时间戳
    timestamp = scrapy.Field()
    title_md5 = scrapy.Field()
    # 来源
    source = scrapy.Field()


class WeiboItem(scrapy.Item):
    title = scrapy.Field()
    # 热搜值
    value = scrapy.Field()
    # 链接地址
    link = scrapy.Field()
    # 创建时间13位时间戳
    timestamp = scrapy.Field()
    title_md5 = scrapy.Field()
    # 来源
    source = scrapy.Field()

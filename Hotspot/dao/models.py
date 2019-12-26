# coding: utf-8
from sqlalchemy import Column, DateTime, String, text, Text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, TINYINT

from dao import Base


class BaiduHot(Base):
    __tablename__ = 'baidu_hot'

    id = Column(INTEGER(11), primary_key=True)
    title = Column(String(255, 'utf8mb4_bin'), nullable=False, comment='标题')
    value = Column(INTEGER(11), nullable=False, comment='热搜指数')
    title_md5 = Column(String(50, 'utf8mb4_bin'), nullable=False, comment='标题MD5加密')
    timestamp = Column(BIGINT(13), nullable=False, comment='13位时间戳(爬取时间)')
    create_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
                         comment='创建时间')
    link = Column(Text(collation='utf8mb4_bin'), comment='连接地址')
    source = Column(TINYINT(2), nullable=False, server_default=text("'1'"), comment='来源')


class WeiboHot(Base):
    __tablename__ = 'weibo_hot'

    id = Column(INTEGER(11), primary_key=True)
    title = Column(String(255, 'utf8mb4_bin'), nullable=False, comment='标题')
    value = Column(INTEGER(11), nullable=False, comment='热搜指数')
    title_md5 = Column(String(50, 'utf8mb4_bin'), nullable=False, comment='标题MD5加密')
    timestamp = Column(BIGINT(13), nullable=False, comment='13位时间戳(爬取时间)')
    create_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
                         comment='创建时间')
    link = Column(Text(collation='utf8mb4_bin'), comment='连接地址')
    source = Column(TINYINT(2), nullable=False, server_default=text("'1'"), comment='来源')
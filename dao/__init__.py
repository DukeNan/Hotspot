import os

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from Hotspot.settings import (DB_HOST,
                              DB_NAME,
                              DB_PORT,
                              DB_USER,
                              DB_PASSWORD)

DB_URL = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4'

engine = create_engine(
    DB_URL,
    max_overflow=0,  # 超过连接池大小外最多创建连接
    pool_size=7,  # 连接池大小
    pool_timeout=30,  # 池中没有线程最多等待的时间，否则报错
    pool_recycle=280  # 多久之后对线程池中的线程进行一次连接的回收（重置）
)

session_maker = sessionmaker(bind=engine)
session = session_maker()

Base = declarative_base()

if __name__ == '__main__':
    # conn = session
    # query = conn.execute('select * from baidu_hot')
    # print(query.fetchall())
    ...

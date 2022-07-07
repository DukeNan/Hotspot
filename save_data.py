import datetime

from dao import session
from dao.iinflux import client
from dao.models import BaiduHot, WeiboHot


class Clear:
    def __init__(self):
        self.influx_client = client
        # mysql 连接
        self.session = session

    def __del__(self):
        self.session.close()
        self.influx_client.close()

    def update2mysql(self, Model, title_md5, value):
        """更新数据到mysql"""
        self.session.query(Model).filter(Model.title_md5 == title_md5). \
            update({"value": value})

    def get_db_data(self, Model, days=-1):
        """
        从MySQL中获取昨天的数据
        :param days: 默认-1，昨天
        :return:
        """
        yesterday = datetime.datetime.now().date() + datetime.timedelta(days=days)
        start = yesterday.strftime('%Y-%m-%d 00:00:00')
        end = yesterday.strftime('%Y-%m-%d 23:59:59')
        queryset = self.session.query(Model).filter(Model.create_time.between(start, end)).all()
        return queryset

    def get_max_value(self, measurement, title_md5):
        """
        从influxdb中获取最大值
        :param measurement:
        :param title_md5:
        :return:
        """
        max_value = 0
        influx_sql = f"select max(value), title_md5 from {measurement} where title_md5='{title_md5}'"
        query = self.influx_client.query(influx_sql)
        data_list = list(query.get_points())
        if data_list:
            max_value = data_list[0].get("max", 0)
        return max_value

    def run(self, measurement, Model):
        data_list = self.get_db_data(Model)
        for item in data_list:
            max_value = self.get_max_value(measurement, item.title_md5)
            if max_value > item.value:
                print(f'更新数据：{item.title_md5},  跟新前：{item.value}，更新后：{max_value}')
                self.update2mysql(Model, item.title_md5, max_value)
        self.session.commit()


if __name__ == '__main__':
    import time

    start = time.time()
    li = [
        {'measurement': 'baidu', 'Model': BaiduHot},
        {'measurement': 'weibo', 'Model': WeiboHot},
    ]
    print('===========开始更新=============')
    clear = Clear()
    for item in li:
        print(f'+++++++++开始：{item["measurement"]}')
        clear.run(**item)
        print(f'+++++++++结束：{item["measurement"]}')
    t = time.time() - start
    print('===========更新结束=============')
    print("用时：%.4f秒" % t)

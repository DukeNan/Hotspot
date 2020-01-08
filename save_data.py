from dao import session
from dao.models import BaiduHot, WeiboHot
from dao.iinflux import client
from threading import Thread


class Clear:
    def __init__(self):
        self.influx_client = client
        # mysql 连接
        self.session = session

    def __del__(self):
        # self.session.commit()
        self.session.close()
        self.influx_client.close()

    def data_from_influx(self, days, measurement):
        """
        从influxdb查询几天以前的数据
        """
        influx_sql = f""" select max(value),title_md5  from {measurement} \
        where time < now() -{days}d group by "title_md5" """
        query = self.influx_client.query(influx_sql)
        return query.get_points()

    def update2mysql(self, Model, title_md5, value):
        """更新数据到mysql"""
        self.session.query(Model).filter(Model.title_md5 == title_md5, Model.is_max == False). \
            update(dict(value=value, is_max=True))

    def run(self, measurement, Model):
        influx_data = self.data_from_influx(days=7, measurement=measurement)
        for item in influx_data:
            self.update2mysql(Model=Model, title_md5=item['title_md5'], value=item['max'])

        self.session.commit()

    def thread_run(self):
        li = [
            {'measurement': 'baidu', 'Model': BaiduHot},
            {'measurement': 'weibo', 'Model': WeiboHot},
        ]
        threads = []
        for i in li:
            t = Thread(target=self.run, kwargs=i)
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        print('==================更新完成========================')


if __name__ == '__main__':
    import time
    start = time.time()
    li = [
        {'measurement': 'baidu', 'Model': BaiduHot},
        {'measurement': 'weibo', 'Model': WeiboHot},
    ]
    clear = Clear()
    for item in li:
        clear.run(**item)
    t = time.time() - start
    print(t)


    # clear = Clear()
    # clear.thread_run()

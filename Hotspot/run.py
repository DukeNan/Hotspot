from multiprocessing import Process
from scrapy import cmdline

t1 = Process(target=cmdline.execute, args=('scrapy crawl baidu'.split(),))
t2 = Process(target=cmdline.execute, args=('scrapy crawl weibo'.split(),))

t1.start()
t2.start()

t1.join()
t2.start()

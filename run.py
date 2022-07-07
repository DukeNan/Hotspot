from datetime import datetime
from pathlib import Path

log_path = Path(__file__).parent.joinpath('logs')
if not log_path.exists():
    log_path.mkdir(parents=True)

now = datetime.now()
log_filename = 'spider_{}.log'.format(now.strftime("%Y%m%d"))

import os

os.system(f'scrapy crawl baidu --logfile=./logs/{log_filename}')
os.system(f'scrapy crawl weibo --logfile=./logs/{log_filename}')

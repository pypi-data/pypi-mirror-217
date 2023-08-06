from time import sleep

import loguru
from loguru import logger
# HTTP Method: GET(), POST()
import requests as rq
# 導入 BeautifulSoup module: 解析 HTML 語法工具
from bs4 import BeautifulSoup as BS
import requests
import time
import json
import datetime
from lxml import etree
import csv
import urllib3
from loguru import logger

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362',
}


class crawler_cnyes:

    def __init__(self, version=1):
        self.datetime_start = datetime.datetime.today()
        self.datetime_end = datetime.datetime.today()

        self.list_news = []
        self.version = version

    @logger.catch
    def fetch(self,
              datetime_start: datetime.datetime = datetime.datetime.today().replace(hour=0, minute=0, second=0),
              datetime_end: datetime.datetime = datetime.datetime.today() + datetime.timedelta(days=1)):

        self.datetime_start = datetime_start
        self.datetime_end = datetime_end

        if self.version == 1:
            url = f'https://api.cnyes.com/media/api/v1/newslist/category/tw_stock?startAt={int(self.datetime_start.timestamp())}&endAt={int(self.datetime_end.timestamp())}&limit=100'
        else:
            url = f'https://news.cnyes.com/api/v3/news/category/tw_stock?startAt={int(self.datetime_start.timestamp())}' \
                  f'&endAt={int(self.datetime_end.timestamp())}&limit=100'
        logger.info(url)
        res = requests.get(url, headers)
        ret = json.loads(res.text)

        list_news = []
        for x in ret['items']['data']:
            title = x['title']
            str_dt = datetime.datetime.fromtimestamp(x['publishAt'])
            # logger.info(f'{str_dt} {title}')
            list_news.append(f'{str_dt} {title}')

        return list_news

    def fetch_new(self):

        list_news_new = []
        list_news = self.fetch()
        for x in list_news:
            if x not in self.list_news:
                list_news_new.append(x)
        self.list_news = list_news

        return list_news_new


if __name__ == '__main__':
    from time import sleep

    cynes1 = crawler_cnyes(1)
    cynes3 = crawler_cnyes(3)
    while True:
        news = cynes1.fetch_new()
        print(news)

        news = cynes3.fetch_new()
        print(news)

        sleep(20)


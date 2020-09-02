# -*- coding: utf-8 -*-

import json
import scrapy
from scrapy_redis.spiders import RedisSpider, RedisCrawlSpider


class MysiteSpider(RedisCrawlSpider):
    name = 'mysite'

    def make_requests_from_url(self, data: str):
        '''
        data就是放入 mysite:start_urls 中的任务
        :param data:
        :return:
        '''
        req_data = json.loads(data)
        url = req_data['url']

        # 此处也可以改为post请求
        return scrapy.Request(
            url,
            meta={'req_data': req_data}
        )

    def parse(self, response):
        print(response.text)
        print(response.meta)
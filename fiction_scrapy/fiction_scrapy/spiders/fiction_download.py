# -*- coding=utf-8 -*-
import json
import unicodedata

import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy_redis.spiders import RedisCrawlSpider

# lpush book_url '{"url":"http://www.shuquge.com/txt/128294/index.html", "table_name":"tb_75", "book_id":"75"}'


class FictionDownload(RedisCrawlSpider):
    name = 'fiction_download'
    redis_key = 'book_url'

    rules = (
        Rule(LinkExtractor(allow=r'\d+.html',
                           restrict_xpaths="//dl/dt[2]/following-sibling::dd[1]"),
             callback='parse_page', follow=True),
        Rule(LinkExtractor(allow=r'\d+.html',
                           restrict_xpaths="//div[@class='page_chapter']/ul/li/a[contains(text(), '下一章')]"),
             callback='parse_page', follow=True),
    )

    def make_requests_from_url(self, data: str):  # 重写该方法，将redis传递的book_data添加到self
        request_data = json.loads(data.replace("'", '"'))  # 将 ' 替换为 "
        url = request_data['url']
        table_name = request_data['table_name']
        book_id = request_data['book_id']
        self.book_data = {'table_name': table_name, 'book_id': book_id}
        return scrapy.Request(url)

    def parse_page(self, response):  # 页面处理
        item = {'chapter_name': response.xpath("string(//div[@class='content']/h1)").extract_first()}
        content = response.xpath('//*[@id="content"]').extract_first()
        item['content'] = unicodedata.normalize('NFKC', content).encode('utf-8')  # 替换乱码
        item['book_id'] = self.book_data.get('book_id')
        item['table_name'] = self.book_data.get('table_name')
        yield item

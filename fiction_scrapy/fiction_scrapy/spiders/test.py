import unicodedata

import scrapy
from lxml import etree
from scrapy_redis.spiders import RedisSpider

from fiction_scrapy.items import FictionScrapyItem


class Test(RedisSpider):
    name = 'test'
    redis_key = 'book_url'

    def parse(self, response, *args, **kwargs):
        chapter_list = response.xpath('//dl/dt[2]/following-sibling::dd/a/@href').extract()
        num = 0
        for chapter in chapter_list:
            # print(chapter)
            num += 1
            yield scrapy.Request(url='http://www.shuquge.com/txt/127797/' + chapter, callback=self.parse_detail,
                                 meta={'num': num})

    def parse_detail(self, resp):
        item = FictionScrapyItem()
        num = resp.meta['num']
        item['chapter_name'] = resp.xpath("string(//div[@class='content']/h1)").extract_first()
        content = resp.xpath('//*[@id="content"]').extract_first()
        item['content'] = unicodedata.normalize('NFKC', content)  # 替换乱码
        item['book_id'] = 26
        item['chapter_id'] = num
        yield item
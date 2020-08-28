# -*- coding=utf-8 -*-
import unicodedata

from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy_redis.spiders import RedisCrawlSpider

from fiction_scrapy.items import FictionScrapyItem


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

    def parse_page(self, response):  # 页面处理
        item = FictionScrapyItem()
        item['chapter_name'] = response.xpath("string(//div[@class='content']/h1)").extract_first()
        content = response.xpath('//*[@id="content"]').extract_first()
        item['content'] = unicodedata.normalize('NFKC', content)  # 替换乱码
        item['book_id'] = 26
        yield item

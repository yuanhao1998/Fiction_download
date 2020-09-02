# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FictionScrapyItem(scrapy.Item):
    chapter_name = scrapy.Field(),
    content = scrapy.Field(),
    book_id = scrapy.Field(),
    table_name = scrapy.Field()
# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy_djangoitem import DjangoItem
from book.models import Chapter


class FictionScrapyItem(DjangoItem):  # 添加django模型类
    django_model = Chapter

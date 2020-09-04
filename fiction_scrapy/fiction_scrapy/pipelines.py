# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymysql

from fiction_scrapy.settings import PYMYSQL


class FictionScrapyPipeline:

    def process_item(self, item, spider):  
        conn = pymysql.connect(**PYMYSQL)
        sql = 'INSERT INTO %s' % item['table_name'] + '(book_id,chapter_name,content)' + ' VALUES (%s, %s, %s)'
        with conn.cursor() as cursor:
            cursor.execute(sql, (item['book_id'], item['chapter_name'], item['content']))
        conn.commit()
        return item

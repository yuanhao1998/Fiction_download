import logging

from django.db import transaction
from django.http import QueryDict
from django_redis import get_redis_connection
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from book.models import Book
from bookshelves.models import BookShelves
from bookshelves.serializers import BookShelvesSerializer
from utils.completion_url import Completion_URL
from utils.pymysql_conn import Conn

logger = logging.getLogger('django')


class BookShelvesModelViewSet(ModelViewSet):  # 书架管理
    serializer_class = BookShelvesSerializer

    def list(self, request, *args, **kwargs):
        bookshelves_list = BookShelves.objects.filter(user=self.request.user)
        book_list = []
        conn = Conn()
        for bookshelves in bookshelves_list:
            book = bookshelves.book
            if not bookshelves.chapter_id:
                chapter = None
            else:
                table_name = 'tb_' + str(book.id)
                query = 'SELECT * FROM %s' % table_name + ' WHERE id = %s'
                conn.execute(query, bookshelves.chapter_id)
                chapter = conn.fetchone()
            book_list.append({
                'book_name': book.book_name,
                'author': book.author,
                'book_id': book.id,
                'chapter_id': chapter.get('id') if chapter else None,
                'chapter_name': chapter.get('chapter_name') if chapter else '您还未开始阅读'
            })
        return Response({
            'errno': 0,
            'errmsg': 'OK',
            'data': book_list
        })

    def create(self, request, *args, **kwargs):
        book_data = QueryDict.dict(request.data)  # 将QueryDict转换为dict，防止使用**时传递值转换为列表
        with transaction.atomic():  # 因为两表都需修改，为防止更新出错，开启事务
            # noinspection PyBroadException
            try:
                save_id = transaction.savepoint()  # 保存点
                if not Book.objects.filter(href=book_data.get('href')):  # 验证是否爬取过该书籍
                    book = Book.objects.create(**book_data)  # 添加到book表
                    table_name = 'tb_' + str(book.id)  # 生成该本书籍的表名
                else:
                    return Response({
                        'errno': 4003,
                        'errmsg': 'The book already exists your bookshelves'
                    })
                bookshelves_data = {  # 构造bookshelves要使用的数据
                    'user_id': request.user.id,
                    'book_id': book.id
                }
                serializer = self.serializer_class(data=bookshelves_data)
                if serializer.is_valid():
                    serializer.save()  # 添加到bookshelves表
                    href = Completion_URL(book.href)
                    conn = Conn()  # 新爬取的书籍需要建表
                    query = "CREATE TABLE IF NOT EXISTS %s (" \
                            "id INT auto_increment PRIMARY KEY ," \
                            "book_id INT NOT NULL," \
                            "chapter_name VARCHAR(100) NOT NULL," \
                            "content LONGTEXT NOT NULL," \
                            "is_delete TINYINT(1) DEFAULT 0 NOT NULL)" % table_name
                    conn.execute(query)
                    # 发送数据到redis，开始爬取书籍
                    redis_conn = get_redis_connection('default')
                    redis_conn.lpush("book_url", str({"url": href, "table_name": table_name, "book_id": book.id}))
                    transaction.savepoint_commit(save_id)
                    return Response({
                        'errno': 0,
                        'errmsg': 'OK'
                    })
                raise  # 如果验证失败，进入异常处理
            except Exception:
                logger.error(Exception)
                transaction.savepoint_rollback(save_id)  # 回滚数据
                conn = Conn()
                query = 'DROP TABLE %s' % table_name
                conn.execute(query)
                return Response({
                    'errno': 4006,
                    'errmsg': 'Failed to add data'
                })
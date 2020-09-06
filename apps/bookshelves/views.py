from django.http import QueryDict
from django_redis import get_redis_connection
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from book.models import Book
from bookshelves.models import BookShelves
from bookshelves.serializers import BookShelvesSerializer
from source_code.settings.dev import logger
from utils.completion_url import Completion_URL
from utils.pymysql_conn import Conn
from utils.sql_manage import book_query1, create_book_table, bookshelves_query1, bookshelves_query3


class BookShelvesModelViewSet(ModelViewSet):  # 书架管理
    serializer_class = BookShelvesSerializer

    def list(self, request, *args, **kwargs):
        book_list = []
        conn = Conn()
        conn.execute(bookshelves_query3, request.user.id)
        bookshelves_list = conn.fetchall()
        for bookshelves in bookshelves_list:
            if not bookshelves.get('chapter_id'):  # 如果没有阅读记录
                chapter = None
            else:
                table_name = 'tb_' + str(bookshelves.get('book_id'))
                query = 'SELECT chapter_name FROM %s' % table_name + ' WHERE id = %s'
                conn.execute(query, bookshelves.get('chapter_id'))
                chapter = conn.fetchone()  # 获取相应章节的内容
            book_list.append({**bookshelves, **chapter})
        return Response({
            'errno': 0,
            'errmsg': 'OK',
            'data': book_list
        })

    def create(self, request, *args, **kwargs):
        book_data = QueryDict.dict(request.data)  # 将QueryDict转换为dict，防止使用**时传递值转换为列表
        conn = Conn()
        # noinspection PyBroadException
        try:
            conn.execute(book_query1, book_data.get('href'))  # 判断该书籍是否爬取过
            book_id = conn.fetchone().get('book_id')

            if not book_id:  # 如果该书籍未被爬取过
                book = Book.objects.create(**book_data)  # 添加新的书籍到book表
                table_name = 'tb_' + str(book.id)
                href = Completion_URL(book.href)
                create_book = create_book_table % table_name
                conn.execute(create_book)  # 新建表存储
                # 发送数据到redis，开始爬取书籍
                redis_conn = get_redis_connection('default')
                redis_conn.lpush("book_url", str({"url": href, "table_name": table_name, "book_id": book.id}))

            conn.execute(bookshelves_query1, (request.user.id, book_id))

            if conn.rowcount():  # 如果用户已经添加到书籍
                return Response({
                    'errno': 4003,
                    'errmsg': 'The book already exists your bookshelves'
                })
            else:  # 添加到书架
                bookshelves_data = {  # 构造bookshelves要使用的数据
                    'user_id': request.user.id,
                    'book_id': book_id
                }
                serializer = self.serializer_class(data=bookshelves_data)

                if serializer.is_valid():
                    serializer.save()  # 添加到bookshelves表

                    return Response({
                        'errno': 0,
                        'errmsg': 'OK'
                    })

            raise
        except Exception:
            conn.rollback()
            logger.error(Exception)
            return Response({
                'errno': 4006,
                'errmsg': 'Failed to add data'
            })
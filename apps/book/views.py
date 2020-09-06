from django.forms import model_to_dict
from django_redis import get_redis_connection
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from book.serializers import BookSerializer
from source_code.settings.dev import logger
from utils.pymysql_conn import Conn
from utils.sql_manage import book_query2, bookshelves_query2, select_book_table


class BookCreateView(CreateAPIView):  # 添加书籍
    serializer_class = BookSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():  # 验证书籍数据、以及该链接是否已爬取过
            book = serializer.save()
            return Response(model_to_dict(book))  # 返回保存的书籍数据
        return Response({
            'errno': 4003,
            'errmsg': 'The book already exists'
        })


class BookReadView(APIView):  # 继续阅读

    def get(self, request):
        book_id = request.query_params.get('book_id')
        chapter_id = request.query_params.get('chapter_id')
        table_name = 'tb_' + str(book_id)
        conn = Conn()
        conn.execute(book_query2, book_id)
        href = conn.fetchone().get('href')
        redis_conn = get_redis_connection('default')
        redis_conn.lpush("book_url", str({"url": href, "table_name": table_name, "book_id": book_id}))
        # noinspection PyBroadException
        try:
            if not chapter_id or chapter_id == '' or chapter_id == 'null':
                query = 'SELECT * FROM %s WHERE id = 1' % table_name
                chapter_id = 1
                conn.execute(query)
                chapter = conn.fetchone()  # 获取到的类型为dict
            else:
                query = 'SELECT id, chapter_name, content FROM %s' % table_name + ' WHERE id = %s'
                conn.execute(query, chapter_id)
                chapter = conn.fetchone()
        except Exception:
            logger.error(Exception)
            return Response({
                'errno': 4001,
                'errmsg': 'database query error'
            })
        # noinspection PyBroadException
        try:
            conn.execute(bookshelves_query2, (chapter_id, book_id))
            return Response({'errno': 0, 'errmsg': 'OK', **chapter})
        except Exception:
            logger.error(Exception)
            conn.rollback()
            return Response({
                'errno': 4007,
                'errmsg': 'database update error'

            })


class BookListAPIView(APIView):  # 返回章节列表

    def get(self, request, book_id):
        conn = Conn()
        table_name = 'tb_' + str(book_id)
        query = select_book_table % table_name
        conn.execute(query)
        data = []
        for value in conn.fetchall():
            data.append(value)
        return Response({
            'errno': 0,
            'errmsg': 'OK',
            'data': data
        })

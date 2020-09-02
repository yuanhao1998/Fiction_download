import logging

from django.forms import model_to_dict
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response

from book.serializers import BookSerializer, BookListSerializer
from utils.pymysql_conn import Conn

logger = logging.getLogger('django')


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


class BookReadView(ListAPIView):  # 继续阅读

    def list(self, request, *args, **kwargs):
        book_id = request.query_params.get('book_id')
        chapter_id = request.query_params.get('chapter_id')
        table_name = 'tb_' + book_id
        conn = Conn()
        # noinspection PyBroadException
        try:
            if not chapter_id or chapter_id == '' or chapter_id == 'null':
                query = 'SELECT * FROM %s WHERE id = 1' % table_name
                chapter_id = 1
                conn.execute(query)
                chapter = conn.fetchone()  # 获取到的类型为dict
            else:
                query = 'SELECT * FROM %s' % table_name + ' WHERE id = %s'
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
            query = 'UPDATE tb_bookshelves SET chapter_id = %s WHERE book_id = %s'
            conn.execute(query, (chapter_id, book_id))
            return Response({
                'errno': 0,
                'errmsg': 'OK',
                'title': chapter.get('chapter_name'),
                'data': chapter.get('content'),
                'id': chapter.get('id')
            })
        except Exception:
            logger.error(Exception)
            conn.rollback()
            return Response({
                'errno': 4007,
                'errmsg': 'database update error'

            })


class BookListAPIView(ListAPIView):  # 返回章节列表
    serializer_class = BookListSerializer

    def list(self, request, *args, **kwargs):
        pass
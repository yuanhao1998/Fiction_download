import json

import requests
from django.db import transaction
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django_redis import get_redis_connection

from bookshelves.models import BookShelves
from bookshelves.serializers import BookShelvesSerializer


class BookShelvesModelViewSet(ModelViewSet):  # 书架管理
    serializer_class = BookShelvesSerializer

    def list(self, request, *args, **kwargs):
        bookshelves_list = BookShelves.objects.filter(user=self.request.user)
        book_list = []
        for bookshelves in bookshelves_list:
            book = bookshelves.book
            chapter = bookshelves.chapter
            book_list.append({
                'book_name': book.book_name,
                'author': book.author,
                'book_id': book.id,
                'chapter_id': chapter.id,
                'chapter_name': chapter.chapter_name
            })
        return Response(book_list)

    def create(self, request, *args, **kwargs):
        book_data = request.data
        with transaction.atomic():  # 因为两表都需修改，为防止更新出错，开启事务
            # noinspection PyBroadException
            try:
                save_id = transaction.savepoint()  # 保存点
                response = requests.post(url='http://127.0.0.1:8000/book/create/', data=book_data)  # 先添加到book表
                book = json.loads(response.content.decode())
                if not book.get('id'):  # 判断是否添加成功
                    return Response(response)
                bookshelves_data = {  # 构造bookshelves要使用的数据
                    'user_id': request.user.id,
                    'book_id': book['id']
                }
                serializer = self.serializer_class(data=bookshelves_data)
                if serializer.is_valid():  # 验证要添加的数据是否符合规则
                    serializer.save()
                    redis_conn = get_redis_connection('default')
                    redis_conn.lpush('book_url', book.get('href'))
                    transaction.savepoint_commit(save_id)  # 提交数据
                    return Response({
                        'errno': 0,
                        'errmsg': 'OK'
                    })
                raise  # 如果验证失败，进入异常处理
            except Exception:
                transaction.savepoint_rollback(save_id)  # 回滚数据
                return Response({
                    'errno': 4006,
                    'errmsg': 'Failed to add data'
                })
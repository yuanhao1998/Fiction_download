from django.forms import model_to_dict
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from book.models import Chapter
from book.serializers import BookSerializer, BookListSerializer


class BookCreateView(CreateAPIView):  # ����鼮
    serializer_class = BookSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():  # ��֤�鼮���ݡ��Լ��������Ƿ�����ȡ��
            book = serializer.save()
            return Response(model_to_dict(book))  # ���ر�����鼮����
        return Response({
            'errno': 4003,
            'errmsg': 'The book already exists'
        })


class BookReadView(APIView):  # ��������

    @staticmethod
    def get(request):
        book_id = request.query_params.get('book_id')
        chapter_id = request.query_params.get('chapter_id')
        chapter = Chapter.objects.get(book_id=book_id, id=chapter_id)
        title = chapter.chapter_name
        data = chapter.content
        return Response({
            'title': title,
            'data': data
        })


class BookListAPIView(ListAPIView):  # �����½��б�
    serializer_class = BookListSerializer

    def list(self, request, *args, **kwargs):
        pass
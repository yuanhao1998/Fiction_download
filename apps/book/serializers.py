from rest_framework import serializers

from book.models import Book


class BookSerializer(serializers.ModelSerializer):  # �鼮���л���
    class Meta:
        model = Book
        fields = '__all__'

        read_only_fields = ('id', 'create_time', 'update_time', 'is_delete')

    def validate(self, attrs):  # ��֤���鼮�Ƿ�����ȡ��
        if Book.objects.filter(href=attrs.get('href')):
            raise serializers.ValidationError('The book already exists')
        return attrs

    def create(self, validated_data):  # ����鼮�����ݿ�
        book_name = validated_data.get('book_name')
        author = validated_data.get('author')
        tags = validated_data.get('tags')
        href = validated_data.get('href')
        if not all([book_name, author, tags, href]):  # У�����
            raise Exception('Missing important parameter')
        try:
            instance = Book.objects.create(**validated_data)  # ������ݵ�book��
        except Exception:
            raise Exception('add book error')
        return instance


class BookListSerializer(serializers.ModelSerializer):  # �½��б����л���
    class Meta:
        model = Book
        fields = ('book_id', 'chapter_name')

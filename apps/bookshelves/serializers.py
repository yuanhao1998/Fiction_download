from rest_framework import serializers

from bookshelves.models import BookShelves


class BookShelvesSerializer(serializers.ModelSerializer):  # 书架序列化器
    book_id = serializers.IntegerField()  # model中此字段为外键，序列化器默认为read_only，有写入需求自行定义
    user_id = serializers.IntegerField()

    class Meta:
        model = BookShelves
        fields = ('id', 'create_time', 'update_time', 'book_id', 'user_id')

        read_only_fields = ('id', 'create_time', 'update_time')

    def create(self, validated_data):  # 添加书籍到数据库
        user_id = validated_data.get('user_id')
        book_id = validated_data.get('book_id')
        if not all([user_id, book_id]):  # 校验参数
            raise Exception('Missing important parameter')
        try:
            instance = BookShelves.objects.create(**validated_data)  # 添加数据到book表
        except Exception:
            raise Exception('add bookshelves error')
        return instance
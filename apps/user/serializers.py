from rest_framework import serializers
from django.contrib.auth.hashers import check_password
from rest_framework.exceptions import ValidationError
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler
from user.models import User


class UserSerializer(serializers.ModelSerializer):  # 用户序列化器
    """
    模型类的username字段中有unique校验
    会导致在is_valid()校验时异常，故自定义该字段
    """
    username = serializers.CharField(max_length=50)

    class Meta:
        model = User
        fields = ('username', 'password')

    def validate(self, attrs):  # 检查登录数据，没有该账号或密码错误时，抛出异常
        username = attrs.get('username')
        password = attrs.get('password')
        # noinspection PyBroadException
        try:
            user = User.objects.get(username=username, is_delete=False)  # 查询是否有该用户
            if user and check_password(password, user.password):
                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)  # 获取token
                return {
                    'token': token,
                    'user': user
                }
            raise
        except Exception:
            raise ValidationError('login error')  # 登录失败抛出异常
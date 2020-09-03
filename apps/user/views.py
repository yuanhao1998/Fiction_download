from django.contrib.auth import login
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework.views import APIView

from source_code.settings.dev import SECRET_KEY, logger
from user.models import User
from user.serializers import UserSerializer


class LoginView(APIView):  # 用户登录验证
    serializer_class = UserSerializer

    def post(self, request):
        request_data = request.data
        username = request_data.get('username')
        password = request_data.get('password')
        if not all([username, password]):  # 校验是否获取到参数
            return Response({
                'errno': 4103,
                'errmsg': 'missing important parameter'
            })
        serializer = self.serializer_class(data=request_data)
        if serializer.is_valid():  # 验证数据
            user = serializer.validated_data['user']
            login(request, user)
            response = Response({
                'errno': 0,
                'errmsg': 'OK',
                'username': username,
                'token': serializer.validated_data['token']
            })
            response.set_cookie('username', user.username, max_age=3600*24)
            return response
        return Response({  # 验证不通过
            'errno': 4104,
            'errmsg': 'user does not exist'
        })


class RegisteredView(APIView):  # 注册
    def post(self, request):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        repeat = data.get('repeat')
        if not all([username, password, repeat]):
            return Response({
                'errno': 4103,
                'errmsg': 'missing important parameter'
            })
        if password != repeat:
            return Response({
                'errno': 4004,
                'errmsg': 'parameter error'
            })
        # noinspection PyBroadException
        try:
            user = User.objects.create(
                username=username,
                password=make_password(password, SECRET_KEY)
            )
            user.save()
            return Response({
                'errno': 0,
                'errmsg': 'OK'
            })
        except Exception:
            logger.error(Exception)
            return Response({
                'errno': 4006,
                'errmsg': 'add data error'
            })
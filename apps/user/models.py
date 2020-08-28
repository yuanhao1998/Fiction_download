from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):  # 用户模型类
    username = models.CharField(verbose_name='用户名', max_length=50, unique=True)
    password = models.CharField(verbose_name='密码', max_length=200)
    last_login = models.DateField(verbose_name='上次登录时间', null=True)
    is_delete = models.BooleanField(verbose_name='是否删除', default=False)

    class Meta:
        db_table = 'tb_user'

    def __str__(self):
        return self.username
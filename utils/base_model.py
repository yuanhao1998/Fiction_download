from django.db import models


class BaseModel(models.Model):  # 模型类的基类
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:  # 声明抽象类，此模型类不会创建表
        abstract = True
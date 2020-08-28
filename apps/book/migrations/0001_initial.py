# Generated by Django 3.1 on 2020-08-14 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('book_name', models.CharField(max_length=100, verbose_name='书名')),
                ('author', models.CharField(max_length=50, verbose_name='作者')),
                ('tags', models.CharField(max_length=100, null=True, verbose_name='标签')),
                ('href', models.CharField(default=None, max_length=500, verbose_name='URL')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
            ],
            options={
                'db_table': 'tb_book',
            },
        ),
    ]

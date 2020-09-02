from django.db import models

from utils.base_model import BaseModel


class Book(BaseModel):  # 书籍模型类
    book_name = models.CharField(verbose_name='书名', max_length=100)
    author = models.CharField(verbose_name='作者', max_length=50)
    tags = models.CharField(verbose_name='标签', max_length=100, null=True)
    href = models.CharField(verbose_name='URL', max_length=500, default=None)
    is_delete = models.BooleanField(verbose_name='是否删除', default=False)

    class Meta:
        db_table = 'tb_book'

    def __str__(self):
        return self.book_name


class Chapter(BaseModel):  # 章节模型类
    book_id = models.IntegerField(verbose_name='书籍id', default=None)
    # chapter_id = models.IntegerField(verbose_name='章节id', default=None)
    chapter_name = models.CharField(verbose_name='章节名', max_length=100)
    content = models.TextField(verbose_name='正文', default=None)
    is_delete = models.BooleanField(verbose_name='是否删除', default=False)

    class Meta:
        db_table = 'tb_chapter'

    def __str__(self):
        return self.chapter_name


class Content(BaseModel):  # 正文模型类
    # chapter = models.ForeignKey(Chapter, verbose_name='章节', on_delete=models.CASCADE)
    content = models.TextField(verbose_name='正文', default=None)

    class Meta:
        db_table = 'tb_content'

    def __str__(self):
        return self.content
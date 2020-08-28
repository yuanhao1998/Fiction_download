from django.db import models

from book.models import Book, Chapter
from user.models import User
from utils.models import BaseModel


class BookShelves(BaseModel):  # 书架模型类
    user = models.ForeignKey(User, verbose_name='用户', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, verbose_name='书籍', on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, verbose_name='章节', on_delete=models.CASCADE)

    class Meta:
        db_table = 'tb_bookshelves'

    def __str__(self):
        return self.user
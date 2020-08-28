from django.urls import path
from . import views

urlpatterns = [
    path('<book_name:book_name>/', views.BookSearchView.as_view()),  # 书籍搜索请求
    path('detail/', views.BookSearchDetailView.as_view())  # 书籍详情查询请求
]

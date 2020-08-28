from django.urls import path

from . import views

urlpatterns = [
    path('create/', views.BookCreateView.as_view()),  # 添加书籍请求
    path('list/', views.BookListAPIView.as_view()),  # 书籍列表请求
    path('', views.BookReadView.as_view()),  # 阅读请求
]
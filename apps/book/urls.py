from django.urls import path

from . import views

urlpatterns = [
    path('create/', views.BookCreateView.as_view()),  # ����鼮����
    path('list/', views.BookListAPIView.as_view()),  # �鼮�б�����
    path('', views.BookReadView.as_view()),  # �Ķ�����
]
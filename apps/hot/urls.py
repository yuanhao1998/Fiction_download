from django.urls import path
from . import views

urlpatterns = [
    path('', views.HotView.as_view()),  # 查询当前热搜
]
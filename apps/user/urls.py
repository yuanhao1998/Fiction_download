from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view())  # 登录请求
]
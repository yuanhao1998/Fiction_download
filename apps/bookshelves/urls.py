from rest_framework.routers import DefaultRouter

from . import views

urlpatterns = [

]

# 添加书架ModelViewSet路由信息
router = DefaultRouter()
router.register('', views.BookShelvesModelViewSet, basename='bookshelves')
urlpatterns += router.urls
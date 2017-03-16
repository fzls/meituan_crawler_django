from django.conf.urls import url

from . import views

urlpatterns = [
    # 首页显示搜索页面
    url(r'^$', views.index, name='index'),
    # TODO: 抓取数据并下载xls文件
    url(r'^search$', views.search, name='search')
]

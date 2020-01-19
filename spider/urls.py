from django.urls import path, re_path
from spider.views import spider

urlpatterns = [
    path('spider/', spider.list, name='spider_list'),
    re_path(r'^spider/start/(\d+)/$', spider.start_scrapy, name='spider_start'),
    re_path(r'^spider/stop/(\d+)/$', spider.stop_scrapy, name='spider_stop'),
]
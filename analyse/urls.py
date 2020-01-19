from django.urls import path, re_path
from analyse.views import analyse, good, comment, sentiment

urlpatterns = [
    path('analyse/home/', analyse.index, name='analyse_home'),
    path('analyse/index/', analyse.index, name='analyse_index'),
    path('analyse/index2/', analyse.index2, name='analyse_index2'),
    path('show/good/', good.list, name='good_list'),
    path('show/comment/', comment.list, name='comment_list'),
    path('analyse/sentiment/', sentiment.list, name='sentiment_list'),
    re_path(r'^show/comment/(\d+)/$', comment.one_good, name='comment_one_good'),
    re_path(r'^show/good/(\d+)/detail/$', good.detail, name='good_detail'),
]
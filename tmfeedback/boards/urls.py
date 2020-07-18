from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.boards_index, name='boards_index'),
    url(r'(?P<pk>\d+)/$', views.board_topics, name='board_topics'),
    url(r'(?P<pk>\d+)/new/$', views.new_topic, name='new_topic'),
]
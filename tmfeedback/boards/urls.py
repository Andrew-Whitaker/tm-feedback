from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.BoardIndexView.as_view(), name='boards_index'),
    path('<int:pk>/', views.board_topics, name='board_topics'),
    path('<int:pk>/new/', views.new_topic, name='new_topic'),
    path('<int:board_pk>/topics/<int:topic_pk>/', views.topic_posts, name='topic_posts'),
    path('<int:board_pk>/topics/<int:topic_pk>/reply/', views.reply_to_topic, name='reply_to_topic'),
    path('<int:board_pk>/topics/<int:topic_pk>/posts/<int:post_pk>/edit/', views.PostUpdateView.as_view(),
         name='edit_post'),
]
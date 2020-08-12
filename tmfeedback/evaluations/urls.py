from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    # path('', views.MeetingListView.as_view(), name='meeting_list'),
    path('create/', views.EvalCreateView.as_view(), name='eval_create'),
]
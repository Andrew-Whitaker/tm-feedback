from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.contrib.auth import views as auth_views

from meetings import views

urlpatterns = [
    path('', views.MeetingListView.as_view(), name='meeting_list'),
    # path('create/', views.MeetingCreateView.as_view(), name='meeting_create'),
    path('<int:meeting_pk>/', views.MeetingDetailView.as_view(), name='meeting-detail'),
    # path('<int:meeting_pk>/update/', views.MeetingUpdateView.as_view(), name='meeting_update'),
    # path('<int:meeting_pk>/delete/', views.MeetingDeleteView.as_view(), name='meeting_delete'),
]

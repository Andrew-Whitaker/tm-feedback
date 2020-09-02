from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.contrib.auth import views as auth_views

from meetings import views
from evaluations import views as eval_views


app_name = 'meetings'
urlpatterns = [
    path('<int:meeting_pk>/', views.MeetingDetailView.as_view(), name='detail'),
    # path('<int:meeting_pk>/update/', views.MeetingUpdateView.as_view(), name='update'),
    # path('<int:meeting_pk>/delete/', views.MeetingDeleteView.as_view(), name='delete'),
]


from django.urls import path

from . import views

urlpatterns = [
    path('', views.ClubIndexView.as_view(), name='club_index'),
]
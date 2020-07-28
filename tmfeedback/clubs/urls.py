from django.urls import path

from . import views

urlpatterns = [
    path('', views.ClubIndexView.as_view(), name='club_index'),
    path('<int:club_id>/', views.ClubHomeView.as_view(), name='club_home'),
    path('<int:club_id>/roster/', views.ClubMemberRoster.as_view(), name='club_member_roster')
]
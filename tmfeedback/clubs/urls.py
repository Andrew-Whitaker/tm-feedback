from django.urls import path, include

from . import views
from meetings import views as meet_views

urlpatterns = [
    path('', views.ClubIndexView.as_view(), name='club_index'),
    path('create/', views.ClubCreateView.as_view(), name='club_create'),
    path('<int:club_id>/', views.ClubHomeView.as_view(), name='club_home'),
    path('<int:club_id>/roster/', views.ClubMemberRoster.as_view(), name='club_member_roster'),
    path('<int:club_id>/membership_requests/', views.ClubManageRequestsView.as_view(), name='club_membership_requests'),
    path('<int:club_id>/meetings/', include('meetings.urls')),
]
from django.urls import path, include

from . import views
from meetings import views as meet_views

meet_urlpatterns = [
    path('', meet_views.MeetingListView.as_view(), name='meeting_index'),
    path('create/', meet_views.MeetingCreateView.as_view(), name='create_meeting'),
]

app_name = 'clubs'
urlpatterns = [
    path('', views.ClubIndexView.as_view(), name='index'),
    path('create/', views.ClubCreateView.as_view(), name='create'),
    path('<int:club_id>/', views.ClubHomeView.as_view(), name='home'),
    path('<int:club_id>/roster/', views.ClubMemberRoster.as_view(), name='member_roster'),
    path('<int:club_id>/membership_requests/', views.ClubManageRequestsView.as_view(), name='membership_requests'),
    path('<int:club_id>/meetings/', include(meet_urlpatterns))
]
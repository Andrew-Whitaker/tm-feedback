"""tmfeedback URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.contrib.auth import views as auth_views

from homepage import views
from users import views as users_views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    path('signup/', users_views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('about/', views.about, name='about'),
    path('boards/', include('boards.urls')),
    path('clubs/', include('clubs.urls', namespace='clubs')),
    path('meetings/', include('meetings.urls.meetings', namespace='meetings')),
    path('performances/', include('meetings.urls.performances', namespace='performances')),
    path('evals/', include('evaluations.urls', namespace='evals')),
    path('users/', include('users.urls')),
    path('admin/', admin.site.urls),
]

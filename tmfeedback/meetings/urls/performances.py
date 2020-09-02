from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.contrib.auth import views as auth_views

from meetings import views
from evaluations import views as eval_views


eval_urlpatterns = [
    path('create/', eval_views.EvalCreateView.as_view(), name='create_eval'),
]

app_name = 'performances'
urlpatterns = [
    path('<int:perf_pk>/', views.PerformanceDetailView.as_view(), name='detail'),
    # path('create/', views.PerformanceCreateView.as_view(), name='create'),
    # path('<int:perf_pk>/update/', views.PerformanceUpdateView.as_view(), name='update'),
    # path('<int:perf_pk>/delete/', views.PerformanceDeleteView.as_view(), name='delete'),
    path('<int:perf_pk>/evals/', include(eval_urlpatterns)),
]

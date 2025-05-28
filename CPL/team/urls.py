from django.urls import path
from . import views  # Ensure you're importing views correctly


app_name = 'team'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('complete-profile/', views.complete_profile, name='complete_profile'),
    path('list/', views.team_list, name='team_list'),
]

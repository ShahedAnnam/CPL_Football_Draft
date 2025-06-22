from django.urls import path
from . import views  # Ensure you're importing views correctly
from .views import team_budget_view

app_name = 'team'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('complete-profile/', views.complete_profile, name='complete_profile'),
    path('list/', views.team_list, name='team_list'),
    path('team/<int:team_id>/budget/', team_budget_view, name='team-budget'),
]

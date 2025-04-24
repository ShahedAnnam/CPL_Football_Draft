from django.urls import path
from . import views  # Import views from the player app


app_name = 'player'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('list/', views.player_list, name='player_list'),
    path('profile/', views.player_profile, name='player_profile'),
    path('complete-profile/', views.complete_profile, name='complete_profile')
]


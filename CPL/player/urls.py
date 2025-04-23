from django.urls import path
from . import views  # Import views from the player app


app_name = 'player'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('player_list/', views.player_list, name='player_list'),
    path('profile/', views.view_profile, name='player_profile'),
    path('profile/edit/', views.create_or_update_profile, name='edit_profile')
]


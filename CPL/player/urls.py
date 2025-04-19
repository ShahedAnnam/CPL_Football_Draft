from django.urls import path
from . import views  # Import views from the player app


app_name = 'player'

urlpatterns = [
     path('dashboard/', views.dashboard, name='dashboard'),
    path('player_list/', views.player_list, name='player_list'),
]


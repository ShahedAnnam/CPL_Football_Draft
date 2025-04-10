from django.urls import path
from . import views  # Import views from the player app


urlpatterns = [
    path('register/', views.register_player, name='register_player'), 
    path('player_list/', views.player_list, name='player_list'),
]


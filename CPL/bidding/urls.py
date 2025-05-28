from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_cards, name='show_cards'),
    path('assign/<int:player_id>/', views.assign_team_and_increment_price, name='assign_player'),
    path('api/player/<int:player_id>/', views.get_player_data, name='get_player_data'),
]

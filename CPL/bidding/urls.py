# bidding/urls.py

from django.urls import path
from . import views


print("DEBUG")
urlpatterns = [
    path('', views.show_cards, name='show_cards'),  # Default page
    path("place-bid/", views.place_bid, name="place_bid"),
    path("perform-short/<int:player_id>/" , views.dopoll , name = "dopoll"), 
    #path('api/player-bid/<int:player_id>/', views.get_player_bid_data, name='get_player_bid_data'),

    #path('api/player-bid/<int:player_id>/', views.get_player_bid_data, name='player_bid_data'),
   
    #path('start/', views.start_bidding, name='start-bidding'),
    #path('place/<int:player_id>/', views.place_bid, name='place-bid'),
    #path('results/', views.bidding_results, name='bidding-results'),
]

from django.urls import path
from . import views


print("DEBUG")

app_name = 'bidding'

urlpatterns = [
    path('', views.bidding_page, name='bidding_page'),
    path('server-time/', views.server_time, name='server_time'),
    path('current-player/place-bid/', views.place_bid, name='place_bid'),
    path('perform-short/<int:player_id>/', views.perform_short, name='perform_short'),
    path('current-player/', views.current_player_view, name='current_player_view'),
    path('current-player/auction-status/', views.auction_status, name='auction_status'),
    path('start-auction/', views.start_auction, name='start-auction'),
    path('pause-auction/', views.pause_auction, name='pause-auction'),
    path('end-auction/', views.end_auction, name='end-auction'),
]

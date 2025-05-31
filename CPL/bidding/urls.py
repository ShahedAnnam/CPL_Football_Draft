# bidding/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_cards, name='show_cards'),  # Default page
    path("place-bid/", views.place_bid, name="place_bid"),
    #path('start/', views.start_bidding, name='start-bidding'),
    #path('place/<int:player_id>/', views.place_bid, name='place-bid'),
    #path('results/', views.bidding_results, name='bidding-results'),
]

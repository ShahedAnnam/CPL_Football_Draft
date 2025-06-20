# authority/urls.py

from django.urls import path
from . import views  # Ensure you're importing views correctly
from .views import set_auction_settings

from . import views

app_name = 'authority'

urlpatterns = [
     path('', views.dashboard, name='dashboard'),
     path('set-auction/', set_auction_settings, name='set_auction_settings'),
    path('', views.dashboard, name='dashboard'),
]

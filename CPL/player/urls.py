from django.urls import path
from . import views

app_name = 'player'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('complete-profile/', views.complete_profile, name='complete_profile'),
    path('list/', views.player_list, name='player_list'),
    path('profile/<int:player_id>/', views.player_profile, name='player_profile'),  # ✅ renamed
]

from django.urls import path
from . import views  # Ensure you're importing views correctly



app_name = 'authority'

urlpatterns = [
     path('dashboard/', views.dashboard, name='dashboard'),
]


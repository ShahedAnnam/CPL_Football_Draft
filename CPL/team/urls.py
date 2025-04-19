from django.urls import path
from . import views  # Ensure you're importing views correctly


app_name = 'team'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
]

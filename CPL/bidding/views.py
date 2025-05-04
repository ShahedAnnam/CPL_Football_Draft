from django.shortcuts import render
from datetime import datetime, timezone as dt_timezone
from django.utils import timezone
from player.models import Player


def show_cards(request):
    # Fetch all player records from the database
    players = Player.objects.all()
    
    # Corrected timezone usage for start time
    start_time = datetime(2025, 5, 4, 7, 43, 0, tzinfo=dt_timezone.utc)  # Example start time
    
    # Get current server time
    current_server_time = timezone.now().isoformat()

    return render(request, 'bidding/home.html', {
        'players': players,
        'start_time': start_time.isoformat(),  # Pass start time to the template
        'current_server_time': current_server_time  # Pass current server time to the template
    })

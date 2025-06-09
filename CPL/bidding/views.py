from django.shortcuts import render
from datetime import datetime, timezone as dt_timezone
from django.utils import timezone
from player.models import Player
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import json

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now


# Hardcoded or configurable START TIME
from django.utils.timezone import datetime, timedelta
import pytz
START_TIME = datetime(2025, 6, 1, 18, 0, 0, tzinfo=pytz.UTC)  # example

def bidding_page(request):
    players = Player.objects.all().order_by('id')  # or any specific order
    context = {
        'players': players,
        'start_time': START_TIME,
        'current_server_time': now().isoformat(),
    }
    return render(request, 'bidding/home.html', context)

def server_time(request):
    return JsonResponse({'server_time': now().isoformat()})

@csrf_exempt
def place_bid(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid method")

    data = json.loads(request.body)
    player_id = data.get("player_id")

    player = get_object_or_404(Player, id=player_id)
    
    # Mock logic (replace with real bidding logic and user/team tracking)
    player.price += 100  # example: increment price
    player.assigned_team = request.user.username if request.user.is_authenticated else "Anonymous"
    player.save()

    return JsonResponse({
        "success": True,
        "price": player.price,
        "assigned_team": player.assigned_team,
    })

def perform_short(request, player_id):
    player = get_object_or_404(Player, id=player_id)
    return JsonResponse({
        "assigned_team": player.assigned_team,
        "price": player.price,
    })
    
    
from datetime import datetime, timedelta, timezone

AUCTION_START_TIME = datetime(2025, 6, 9, 19, 28, 0, tzinfo=timezone.utc)
PLAYER_DURATION = timedelta(seconds=20)

def get_current_player_info():
    now = datetime.now(timezone.utc)
    players = Player.objects.all().order_by('id')
    total_players = players.count()
    auction_end_time = AUCTION_START_TIME + total_players * PLAYER_DURATION

    if now < AUCTION_START_TIME:
        return {
            "status": "not_started",
            "time_until_start": int((AUCTION_START_TIME - now).total_seconds()),
            "total_time_left": 0,
            "time_since_end": 0,
        }

    if now >= auction_end_time:
        return {
            "status": "finished",
            "time_until_start": 0,
            "total_time_left": 0,
            "time_since_end": int((now - auction_end_time).total_seconds()),
        }

    # Auction is active
    delta = now - AUCTION_START_TIME
    round_index = int(delta.total_seconds() // PLAYER_DURATION.total_seconds())
    round_start = AUCTION_START_TIME + round_index * PLAYER_DURATION
    round_end = round_start + PLAYER_DURATION
    seconds_remaining = int((round_end - now).total_seconds())

    player = players[round_index]

    return {
        "status": "active",
        "player": {
            "id": player.id,
            "name": player.name,
            "age": player.age,
            "playing_position": player.playing_position,
            "batch": player.batch,
            "contact_number": player.contact_number,
            "profile_picture_url": player.profile_picture.url if player.profile_picture else None,
            "assigned_team": player.assigned_team,
            "price": player.price,
        },
        "seconds_remaining": seconds_remaining,
        "time_until_start": 0,
        "total_time_left": int((auction_end_time - now).total_seconds()),
        "time_since_end": 0,
    }


def current_player_view(request):
    player_info = get_current_player_info()
    return render(request, 'bidding/currentPlayer.html', {'info': player_info})
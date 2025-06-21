from django.shortcuts import render
from datetime import datetime, timezone as dt_timezone
from django.utils import timezone
from player.models import Player
from team.models import Team
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
from bidding.models import AuctionSettings
from authority.views import increase_player_duration_view



# Hardcoded or configurable START TIME
from django.utils.timezone import datetime, timedelta
import pytz
START_TIME = datetime(2025, 6, 1, 18, 0, 0, tzinfo=pytz.UTC)  # example


def start_auction(request):
    if request.method == 'GET':
        setting = AuctionSettings.objects.first()
        if not setting:
            return JsonResponse({'error': 'No AuctionSettings found'}, status=500)
        setting.start_time = timezone.now()
        setting.save()
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def pause_auction(request):
    if request.method == 'GET':
        # For now, just return success, implement real pause logic later
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def end_auction(request):
    if request.method == 'GET':
        setting = AuctionSettings.objects.first()
        if not setting:
            return JsonResponse({'error': 'No AuctionSettings found'}, status=500)
        setting.end_time = timezone.now()
        setting.save()
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Invalid request'}, status=400)


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

    if not request.user.is_authenticated:
        return JsonResponse({"success": False, "message": "You must be logged in to bid."})

    # load the Team that belongs to the logged-in user
    try:
        bidder_team = Team.objects.get(user=request.user)
    except Team.DoesNotExist:
        return JsonResponse({"success": False, "message": "Your user is not linked to any team."})

    data = json.loads(request.body)
    player = get_object_or_404(Player, id=data.get("player_id"))

    # increment price & assign FK
    player.price += 100
    player.assigned_team = bidder_team
    player.save()

    return JsonResponse({
        "success": True,
        "price": player.price,
        "assigned_team": bidder_team.user.username,
        "assigned_team_id": bidder_team.id,
    })



def perform_short(request, player_id):
    player = get_object_or_404(Player, id=player_id)
    return JsonResponse({
        "assigned_team": player.assigned_team,
        "price": player.price,
    })
    
    
from datetime import datetime, timedelta, timezone

AUCTION_START_TIME = datetime(2025, 6, 9, 21, 58, 0, tzinfo=timezone.utc)
PLAYER_DURATION = timedelta(seconds=20)

def get_current_player_info():
    settings = AuctionSettings.objects.first()
    if settings:
        AUCTION_START_TIME = settings.auction_start_time
        PLAYER_DURATION = settings.player_duration
    else:
        AUCTION_START_TIME = datetime(2025, 6, 9, 19, 28, 0, tzinfo=timezone.utc)
        PLAYER_DURATION = timedelta(seconds=20)
    
    print(AUCTION_START_TIME);
    
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
            "assigned_team": player.assigned_team.user.username if player.assigned_team else "Not bought yet",
            "assigned_team_id": player.assigned_team.id if player.assigned_team else None,
            "price": player.price,
        },
        "seconds_remaining": seconds_remaining,
        "time_until_start": 0,
        "total_time_left": int((auction_end_time - now).total_seconds()),
        "time_since_end": 0,
    }


def current_player_view(request):
    # ... your existing code ...
    logged_in_team_id = None
    if request.user.is_authenticated:
        try:
            logged_in_team_id = request.user.team.id
        except AttributeError:
            logged_in_team_id = None

    context = {
        'logged_in_team_id': logged_in_team_id,
        'user_role': getattr(request.user, 'role', '') if request.user.is_authenticated else '',
        'user_is_authenticated': request.user.is_authenticated,
        # other context variables...
    }
    return render(request, 'bidding/currentPlayer.html', context)


from django.views.decorators.cache import never_cache
@never_cache
def auction_status(request):
    info = get_current_player_info() # returns dict with player, status, etc.
    return JsonResponse(info)
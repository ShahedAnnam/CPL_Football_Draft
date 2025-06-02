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
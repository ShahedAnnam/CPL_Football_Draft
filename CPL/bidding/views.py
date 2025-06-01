from django.shortcuts import render
from datetime import datetime, timezone as dt_timezone
from django.utils import timezone
from player.models import Player
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import json
from player.models import Player

def show_cards(request):
    # Fetch all player records from the database
    players = Player.objects.all()
    
    # Corrected timezone usage for start time
    start_time = datetime(2025, 5, 2, 3, 33, 0, tzinfo=dt_timezone.utc)  # Example start time
    
    # Get current server time
    current_server_time = timezone.now().isoformat()

    return render(request, 'bidding/home.html', {
        'players': players,
        'start_time': start_time.isoformat(),  # Pass start time to the template
        'current_server_time': current_server_time  # Pass current server time to the template
    })

@csrf_exempt  # For test only; prefer @login_required + proper CSRF handling

def place_bid(request):
    if request.method == "POST":
        data = json.loads(request.body)
        player_id = data.get("player_id")

        try:
            player = Player.objects.get(id=player_id)

            # Simulate bid logic
            player.price += 100  # or whatever logic
            player.assigned_team = f"{request.user.username}"  # or fetch from user/session
            player.save()

            return JsonResponse({
                "success": True,
                "message": "Bid placed successfully",
                "assigned_team": player.assigned_team,
                "price": player.price,
            })
        except Player.DoesNotExist:
            return JsonResponse({"success": False, "message": "Player not found"}, status=404)

    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)



def dopoll(request, player_id):
    try:
        player = Player.objects.get(id=player_id)
        data = {
            "assigned_team": player.assigned_team if player.assigned_team else "None",
            "price": player.price if player.price else 0
        }
        return JsonResponse(data)
    except Player.DoesNotExist:
        return JsonResponse({"error": "Player not found"}, status=404)
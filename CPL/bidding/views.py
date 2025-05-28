from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from datetime import datetime, timezone as dt_timezone
from player.models import Player
from django.contrib.auth.decorators import login_required

def show_cards(request):
    players = Player.objects.all()
    start_time = datetime(2025, 5, 27, 9, 54, 0, tzinfo=dt_timezone.utc)
    current_server_time = timezone.now().isoformat()

    return render(request, 'bidding/home.html', {
        'players': players,
        'start_time': start_time.isoformat(),
        'current_server_time': current_server_time
    })

@login_required
def assign_team_and_increment_price(request, player_id):
    if request.user.role != "Team":
        return JsonResponse({"success": False, "error": "Unauthorized"}, status=403)

    player = get_object_or_404(Player, id=player_id)
    team_name = request.user.username

    player.current_price += 100
    player.assigned_team = team_name
    player.save()

    return JsonResponse({
        "success": True,
        "message": f"{player.name} assigned to {team_name} for {player.current_price}",
        "current_price": player.current_price,
        "assigned_team": player.assigned_team
    })

def get_player_data(request, player_id):
    player = get_object_or_404(Player, id=player_id)
    return JsonResponse({
        "current_price": player.current_price,
        "assigned_team": player.assigned_team
    })

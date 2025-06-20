from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from player.models import Player
from team.models import Team

@login_required
def dashboard(request):
    if not hasattr(request.user, 'role') or request.user.role != 'authority':
        raise PermissionDenied  # or redirect somewhere else if you want

    players = Player.objects.all()
    teams = Team.objects.all()

    if request.method == 'POST':
        for player in players:
            category = request.POST.get(f'player_class_{player.id}')
            if category in ['A', 'B', 'C']:
                player.player_class = category
                player.save()
        return redirect('authority:dashboard')

    return render(request, 'authority/dashboard.html', {
        'players': players,
        'teams': teams,
    })

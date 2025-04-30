from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from player.models import Player
from .models import Team
from .forms import TeamForm


def dashboard(request):
    return render(request, 'team/dashboard.html')



@login_required
def complete_profile(request):
    try:
        profile = request.user.team  # Get existing profile
        form = TeamForm(request.POST or None, request.FILES or None, instance=profile)
    except Team.DoesNotExist:
        form = TeamForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('team:dashboard')

    return render(request, 'team/complete_profile.html', {'form': form})




@login_required
def team_list(request):
    teams = Team.objects.all()
    return render(request, 'team/team_list.html', {'teams': teams})

@login_required
def player_list(request):
    batch_filter = request.GET.get('batch', None)
    position_filter = request.GET.get('position', None)

    players = Player.objects.all()

    if batch_filter:
        players = players.filter(batch__icontains=batch_filter)  # use icontains for partial match and case-insensitive

    if position_filter:
        players = players.filter(playing_position=position_filter)

    return render(request, 'player/player_list.html', {
        'players': players,
        'batch_filter': batch_filter,
        'position_filter': position_filter
    })
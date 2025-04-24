from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Player
from .forms import PlayerProfileForm

@login_required
def dashboard(request):
    player = Player.objects.filter(user=request.user).first()
    return render(request, 'player/dashboard.html', {'player': player})

@login_required
def player_list(request):
    players = Player.objects.all()
    return render(request, 'player/player_list.html', {'players': players})

@login_required
def player_profile(request):
    player = Player.objects.filter(user=request.user).first()
    return render(request, 'player/player_profile.html', {'player': player})

@login_required
def complete_profile(request):
    try:
        profile = Player.objects.get(user=request.user)
        form = PlayerProfileForm(request.POST or None, request.FILES or None, instance=profile)
    except Player.DoesNotExist:
        form = PlayerProfileForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('player:dashboard')  # or your desired redirect

    return render(request, 'player/complete_profile.html', {'form': form})
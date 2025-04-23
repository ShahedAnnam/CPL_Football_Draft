from django.shortcuts import render, redirect, get_object_or_404
from .forms import PlayerRegistrationForm
from django.contrib import messages
from .forms import PlayerRegistrationForm  
from .models import Player
from django.contrib.auth.decorators import login_required



def dashboard(request):
    return render(request, 'player/dashboard.html')

def player_list(request):
    players = Player.objects.all()
    return render(request, 'player/player_list.html', {'players': players})

@login_required
def create_or_update_profile(request):
    try:
        player = Player.objects.get(user=request.user)
    except Player.DoesNotExist:
        player = None

    if request.method == 'POST':
        form = PlayerRegistrationForm(request.POST, request.FILES, instance=player)
        if form.is_valid():
            new_player = form.save(commit=False)
            new_player.user = request.user
            new_player.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('dashboard')  # Redirecting to the dashboard instead of player_profile
    else:
        form = PlayerRegistrationForm(instance=player)

    return render(request, 'player/profile_form.html', {'form': form})


@login_required
def view_profile(request):
    player = get_object_or_404(Player, user=request.user)
    return render(request, 'player/profile_view.html', {'player': player})


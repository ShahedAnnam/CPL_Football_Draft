from django.shortcuts import render, redirect
from .forms import PlayerRegistrationForm
from django.contrib import messages
from .forms import PlayerRegistrationForm  
from .models import Player



def player_list(request):
    players = Player.objects.all()
    return render(request, 'player/player_list.html', {'players': players})


def register_player(request):
    if request.method == "POST":
        form = PlayerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('player_list')  # Redirect to success page
    else:
        form = PlayerRegistrationForm()
    
    return render(request, "player/register_player.html", {"form": form})

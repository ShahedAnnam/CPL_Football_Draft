from django.shortcuts import render, redirect
from .forms import PlayerRegistrationForm
from django.contrib import messages
from .forms import PlayerRegistrationForm  
from .models import Player


def dashboard(request):
    return render(request, 'player/dashboard.html')

def player_list(request):
    players = Player.objects.all()
    return render(request, 'player/player_list.html', {'players': players})



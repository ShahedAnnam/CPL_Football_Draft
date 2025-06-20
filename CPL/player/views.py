from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Player
from .forms import PlayerProfileForm

@login_required
def dashboard(request):
    player = Player.objects.filter(user=request.user).first()
    return render(request, 'player/dashboard.html', {'player': player})

@login_required
def player_list(request):
    batch_filter = request.GET.get('batch', None)
    position_filter = request.GET.get('position', None)
    category_filter = request.GET.get('player_category', None)  # changed here

    players = Player.objects.all()

    if batch_filter:
        players = players.filter(batch=batch_filter)
    if position_filter:
        players = players.filter(playing_position=position_filter)
    if category_filter:
        players = players.filter(player_class=category_filter)  # player_class remains, just filter key changed

    all_batches = list(range(45, 61))
    category_choices = Player.CATEGORY_CHOICES  # pass category choices to template

    return render(request, 'player/player_list.html', {
        'players': players,
        'batch_filter': batch_filter,
        'position_filter': position_filter,
        'category_filter': category_filter,  # changed here
        'all_batches': all_batches,
        'category_choices': category_choices,  # changed here
    })

@login_required
def player_profile(request, player_id):  # still shows any profile by ID
    player = get_object_or_404(Player, id=player_id)
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
            return redirect('player:dashboard')

    return render(request, 'player/complete_profile.html', {'form': form})

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
    batch_filter = request.GET.get('batch', None)
    position_filter = request.GET.get('position', None)
    class_filter = request.GET.get('player_class', None) # Get the new class filter

    players = Player.objects.all()

    if batch_filter:
        players = players.filter(batch=batch_filter)

    if position_filter:
        players = players.filter(playing_position=position_filter)

    if class_filter:
        # Assuming 'player_class' is a field in your Player model
        players = players.filter(player_class=class_filter)
    elif class_filter == '': # Handle 'All' option for radio buttons
        players = players # Do nothing, show all

    # Prepare batches for the filter dropdown (45 to 60)
    all_batches = list(range(45, 61))

    return render(request, 'player/player_list.html', {
        'players': players,
        'batch_filter': batch_filter,
        'position_filter': position_filter,
        'class_filter': class_filter, # Pass the new filter
        'all_batches': all_batches,
    })

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
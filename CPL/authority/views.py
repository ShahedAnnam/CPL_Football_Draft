from django.shortcuts import render, redirect
from django.utils.timezone import make_aware, now
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.utils import timezone
from player.models import Player
from team.models import Team
from bidding.models import AuctionSettings


@login_required
def dashboard(request):
    if not hasattr(request.user, 'role') or request.user.role != 'authority':
        raise PermissionDenied

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


@login_required
def set_auction_settings(request):
    settings, created = AuctionSettings.objects.get_or_create(id=1)

    if request.method == 'POST':
        start_time_str = request.POST.get('start_time')
        duration_seconds = request.POST.get('duration')
        budget_amount = request.POST.get('budget')  # 👈 new field

        try:
            # Try parsing the datetime
            try:
                dt = datetime.strptime(start_time_str, "%Y-%m-%dT%H:%M")
            except ValueError:
                dt = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")

            settings.auction_start_time = make_aware(dt)
            settings.player_duration = timedelta(seconds=int(float(duration_seconds)))
            settings.player_default_duration = settings.player_duration
            settings.player_current_index = 0
            settings.auction_end_time = datetime.max.replace(tzinfo=make_aware(datetime.now()).tzinfo)

            settings.save()

            # ✅ Set the new budget value
            if budget_amount:
                budget_amount = int(budget_amount)
                # Set in PlayerCategory (if used globally)
                PlayerCategory.objects.update(budget_of_teams=budget_amount)
                # Update each team's expense budget
                Team.objects.all().update(expense_budget=budget_amount)

        except Exception as e:
            return render(request, 'authority/set_auction.html', {
                'error': f'Invalid input: {e}',
                'current_start': settings.auction_start_time,
                'current_duration': settings.player_duration.total_seconds(),
            })

        return redirect('authority:set_auction_settings')

    return render(request, 'authority/set_auction.html', {
        'current_start': settings.auction_start_time,
        'current_duration': settings.player_duration.total_seconds(),
    })


@login_required
def initialize_player_duration_view(request, seconds):
    try:
        settings, _ = AuctionSettings.objects.get_or_create(id=1)
        settings.player_duration = timedelta(seconds=seconds)
        settings.save()
        return JsonResponse({'message': f'Initialized to {seconds} seconds.'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@login_required
def increase_player_duration_view(request, seconds):
    try:
        settings, _ = AuctionSettings.objects.get_or_create(id=1)
        current = settings.player_duration or timedelta(seconds=0)
        settings.player_duration = current + timedelta(seconds=seconds)
        settings.save()
        return JsonResponse({'message': f'Increased by {seconds} seconds.'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)



from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import PlayerCategory
from team.models import Team  # Adjust import based on your app name

def set_initial_budget(request):
    if request.method == "POST":
        try:
            amount = int(request.POST.get("budget"))

            # ✅ Update PlayerCategory (optional)
            PlayerCategory.objects.update(budget_of_teams=amount)

            # ✅ Update all Teams
            Team.objects.all().update(expense_budget=amount)

            return HttpResponse("Budget successfully updated for all teams.")

        except (ValueError, TypeError):
            return HttpResponse("Invalid budget value.", status=400)

    return render(request, "authority/set_budget.html")

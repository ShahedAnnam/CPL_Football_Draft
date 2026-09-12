from django.shortcuts import render
from datetime import datetime, timezone as dt_timezone
from django.utils import timezone
from player.models import Player
from team.models import Team
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db import transaction
import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
from bidding.models import AuctionSettings
from authority.views import increase_player_duration_view



# Hardcoded or configurable START TIME
from django.utils.timezone import datetime, timedelta
import pytz
START_TIME = datetime(2025, 6, 1, 18, 0, 0, tzinfo=pytz.UTC)  # example


def start_auction(request):
    if request.method == 'GET':
        setting = AuctionSettings.objects.first()
        if not setting:
            return JsonResponse({'error': 'No AuctionSettings found'}, status=500)
        now_ts = timezone.now()

        # FIX: previously Start Auction only reset the timer/index — it left
        # every team's spent budget and every player's price/winner exactly
        # as they were from the last run. So a "new" auction would still
        # carry over the old budgets, and bids would fail with "Not enough
        # budget" even though nothing had actually been bid on yet this run.
        # A fresh Start Auction now really does start from the very beginning:
        if setting.starting_budget:
            Team.objects.all().update(expense_budget=setting.starting_budget)

        for player in Player.objects.all():
            player.assigned_team = None
            # setting price to 100 with assigned_team cleared makes
            # Player.save() re-derive the correct category base price
            # (1000/700/500) itself, same logic used when a category is
            # first assigned from the dashboard.
            player.price = 100
            player.save()

        setting.auction_start_time = now_ts
        setting.player_current_index = 0
        setting.player_start_time = now_ts
        setting.player_duration = setting.player_default_duration
        setting.is_paused = False
        setting.paused_at = None
        setting.save()
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Invalid request'}, status=400)


def pause_auction(request):
    if request.method == 'GET':
        setting = AuctionSettings.objects.first()
        if not setting:
            return JsonResponse({'error': 'No AuctionSettings found'}, status=500)

        if setting.is_paused:
            # Resuming: shift player_start_time forward by however long we were
            # paused, so the remaining time on the clock is preserved instead
            # of being lost or instantly expiring.
            if setting.paused_at:
                pause_length = timezone.now() - setting.paused_at
                setting.player_start_time = setting.player_start_time + pause_length
            setting.is_paused = False
            setting.paused_at = None
        else:
            setting.is_paused = True
            setting.paused_at = timezone.now()

        setting.save()
        return JsonResponse({'success': True, 'paused': setting.is_paused})
    return JsonResponse({'error': 'Invalid request'}, status=400)


def end_auction(request):
    if request.method == 'GET':
        setting = AuctionSettings.objects.first()
        if not setting:
            return JsonResponse({'error': 'No AuctionSettings found'}, status=500)
        # FIX: was writing to `setting.end_time`, which doesn't exist on the
        # model (the real field is `auction_end_time`) — same bug as start_auction.
        setting.auction_end_time = timezone.now()
        setting.player_current_index = Player.objects.count()  # forces "finished" status
        setting.is_paused = False
        setting.paused_at = None
        setting.save()
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Invalid request'}, status=400)


def bidding_page(request):
    players = Player.objects.all().order_by('id')  # or any specific order
    context = {
        'players': players,
        'start_time': START_TIME,
        'current_server_time': now().isoformat(),
    }
    return render(request, 'bidding/home.html', context)

def server_time(request):
    return JsonResponse({'server_time': now().isoformat()})

@csrf_exempt
def place_bid(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid method")

    if not request.user.is_authenticated:
        return JsonResponse({"success": False, "message": "You must be logged in to bid."})

    # load the Team that belongs to the logged-in user
    try:
        bidder_team = Team.objects.get(user=request.user)
    except Team.DoesNotExist:
        return JsonResponse({"success": False, "message": "Your user is not linked to any team."})

    data = json.loads(request.body)

    with transaction.atomic():
        settings = AuctionSettings.objects.select_for_update().first()
        if not settings:
            return JsonResponse({"success": False, "message": "Auction is not configured."})

        if settings.is_paused:
            return JsonResponse({"success": False, "message": "Auction is paused."})

        players = Player.objects.all().order_by('id')
        total_players = players.count()

        if settings.player_current_index >= total_players:
            return JsonResponse({"success": False, "message": "Auction has already finished."})

        player = players[settings.player_current_index]
        # FIX: data.get("player_id") comes from the browser as a JSON string
        # (HTML data-attributes are always strings), while player.id is an
        # int — comparing them directly (`player.id != data.get("player_id")`)
        # was always True, so every bid was being rejected. Cast to int first.
        try:
            submitted_player_id = int(data.get("player_id"))
        except (TypeError, ValueError):
            return JsonResponse({"success": False, "message": "Invalid player."})

        if player.id != submitted_player_id:
            return JsonResponse({
                "success": False,
                "message": "This player is not currently up for bidding — the round may have just changed, refresh the page.",
            })

        if bidder_team.expense_budget < player.price + 100:
            return JsonResponse({"success": False, "message": "Not enough budget left to bid this player"})

        player.price += 100
        player.assigned_team = bidder_team
        player.save()

        # timing: extend the current round so a last-second bid gives everyone
        # a fresh window to respond (anti-snipe), same behaviour as before.
        settings.player_duration = (now() - settings.player_start_time) + settings.auction_increase_time
        settings.save()

    return JsonResponse({
        "success": True,
        "price": player.price,
        "assigned_team": bidder_team.user.username,
        "assigned_team_id": bidder_team.id,
    })



def perform_short(request, player_id):
    player = get_object_or_404(Player, id=player_id)
    return JsonResponse({
        "assigned_team": player.assigned_team,
        "price": player.price,
    })
    
    
from datetime import datetime, timedelta, timezone

AUCTION_START_TIME = datetime(2025, 6, 9, 21, 58, 0, tzinfo=timezone.utc)
PLAYER_DURATION = timedelta(seconds=20)
DEFAULT_PLAYER_DURATION = datetime(2025, 6, 9, 21, 58, 0, tzinfo=timezone.utc)

def get_current_player_info2():
    settings = AuctionSettings.objects.first()
    if settings:
        AUCTION_START_TIME = settings.auction_start_time
        PLAYER_DURATION = settings.player_duration
    else:
        AUCTION_START_TIME = datetime(2025, 6, 9, 19, 28, 0, tzinfo=timezone.utc)
        PLAYER_DURATION = timedelta(seconds=20)
    
    print(AUCTION_START_TIME);
    
    now = datetime.now(timezone.utc)
    players = Player.objects.all().order_by('id')
    total_players = players.count()
    auction_end_time = AUCTION_START_TIME + total_players * PLAYER_DURATION

    if now < AUCTION_START_TIME:
        return {
            "status": "not_started",
            "time_until_start": int((AUCTION_START_TIME - now).total_seconds()),
            "total_time_left": 0,
            "time_since_end": 0,
        }

    if now >= auction_end_time:
        return {
            "status": "finished",
            "time_until_start": 0,
            "total_time_left": 0,
            "time_since_end": int((now - auction_end_time).total_seconds()),
        }

    # Auction is active
    delta = now - AUCTION_START_TIME
    round_index = int(delta.total_seconds() // PLAYER_DURATION.total_seconds())
    round_start = AUCTION_START_TIME + round_index * PLAYER_DURATION
    round_end = round_start + PLAYER_DURATION
    seconds_remaining = int((round_end - now).total_seconds())

    player = players[round_index]
    
    return {
        "status": "active",
        "player": {
            "id": player.id,
            "name": player.name,
            "age": player.age,
            "playing_position": player.playing_position,
            "batch": player.batch,
            "contact_number": player.contact_number,
            "profile_picture_url": player.profile_picture.url if player.profile_picture else None,
            "assigned_team": player.assigned_team.user.username if player.assigned_team else "Not bought yet",
            "assigned_team_id": player.assigned_team.id if player.assigned_team else None,
            "price": player.price,
        },
        "seconds_remaining": seconds_remaining,
        "time_until_start": 0,
        "total_time_left": int((auction_end_time - now).total_seconds()),
        "time_since_end": 0,
    }


from datetime import datetime, timedelta
from django.utils import timezone
from .models import AuctionSettings
def get_current_player_info(request):
    with transaction.atomic():
        # FIX: select_for_update() locks this row for the duration of the
        # transaction. currentPlayer.html polls this endpoint every 500ms from
        # every logged-in team's browser at once — without a lock, two nearly
        # simultaneous requests could both see "round has ended" and both run
        # the transition below, double-deducting a team's budget or skipping
        # a player. Locking serializes them so only one performs the transition.
        settings = AuctionSettings.objects.select_for_update().first()

        if not settings:
            return {
                "status": "error",
                "message": "Auction settings not found."
            }

        now = timezone.now()
        AUCTION_START_TIME = settings.auction_start_time
        PLAYER_DURATION = settings.player_duration
        DEFAULT_PLAYER_DURATION = settings.player_default_duration
        CURRENT_INDEX = settings.player_current_index
        PLAYER_START_TIME = settings.player_start_time

        players = Player.objects.all().order_by('id')
        total_players = players.count()

        if total_players == 0:
            return {
                "status": "no_players",
                "message": "No players available."
            }

        if now < AUCTION_START_TIME:
            return {
                "status": "not_started",
                "time_until_start": int((AUCTION_START_TIME - now).total_seconds()),
                "current_index": CURRENT_INDEX,
                "total_players": total_players,
            }

        if CURRENT_INDEX >= total_players:
            return {
                "status": "finished",
                "time_since_end": int((now - settings.auction_end_time).total_seconds()),
                "current_index": CURRENT_INDEX,
                "total_players": total_players,
            }

        # FIX: while the auction is paused, freeze the clock entirely — skip
        # the round-transition logic below so no budget gets deducted and no
        # player gets skipped while paused, and report the time that was left
        # at the moment of pausing instead of live time.
        if settings.is_paused:
            player = players[CURRENT_INDEX]
            frozen_reference = settings.paused_at or now
            round_end = settings.player_start_time + PLAYER_DURATION
            seconds_remaining = max(0, int((round_end - frozen_reference).total_seconds()))

            user_expense_budget = None
            if request and request.user.is_authenticated:
                try:
                    team = Team.objects.get(user=request.user)
                    user_expense_budget = team.expense_budget
                except Team.DoesNotExist:
                    pass

            return {
                "status": "paused",
                "player": {
                    "id": player.id,
                    "name": player.name,
                    "age": player.age,
                    "playing_position": player.playing_position,
                    "batch": player.batch,
                    "contact_number": player.contact_number,
                    "profile_picture_url": player.profile_picture.url if player.profile_picture else None,
                    "assigned_team": player.assigned_team.user.username if player.assigned_team else "Not bought yet",
                    "assigned_team_id": player.assigned_team.id if player.assigned_team else None,
                    "price": player.price,
                },
                "seconds_remaining": seconds_remaining,
                "current_index": CURRENT_INDEX,
                "total_players": total_players,
                "user_expense_budget": user_expense_budget,
            }

        # 👇 If player_start_time is still default (unset), set it now
        if settings.player_start_time < AUCTION_START_TIME:
            settings.player_start_time = now
            settings.save()

        round_start = settings.player_start_time
        round_end = round_start + PLAYER_DURATION
        player = players[CURRENT_INDEX]
        transition = False

        if now >= round_end:
            # 💰 Cut budget if assigned
            if player.assigned_team:
                bidder_team = player.assigned_team
                if bidder_team.expense_budget >= player.price:
                    bidder_team.expense_budget -= player.price
                    bidder_team.save()

            # Move to next player
            CURRENT_INDEX += 1
            settings.player_current_index = CURRENT_INDEX
            settings.player_start_time = now
            settings.player_duration = DEFAULT_PLAYER_DURATION
            settings.auction_end_time = now
            settings.save()
            transition = True

            if CURRENT_INDEX >= total_players:
                return {
                    "status": "finished",
                    "time_since_end": 0,
                    "current_index": CURRENT_INDEX,
                    "total_players": total_players,
                }

            # 👇 Get next player safely
            player = players[CURRENT_INDEX]
            round_end = now + DEFAULT_PLAYER_DURATION

        # ⏱ Clamp time remaining
        seconds_remaining = max(0, int((round_end - now).total_seconds()))

        # 🧾 Team budget info
        user_team_id = None
        user_expense_budget = None
        if request and request.user.is_authenticated:
            try:
                team = Team.objects.get(user=request.user)
                user_team_id = team.id
                user_expense_budget = team.expense_budget
            except Team.DoesNotExist:
                pass

        return {
            "status": "active",
            "transition": transition,
            "player": {
                "id": player.id,
                "name": player.name,
                "age": player.age,
                "playing_position": player.playing_position,
                "batch": player.batch,
                "contact_number": player.contact_number,
                "profile_picture_url": player.profile_picture.url if player.profile_picture else None,
                "assigned_team": player.assigned_team.user.username if player.assigned_team else "Not bought yet",
                "assigned_team_id": player.assigned_team.id if player.assigned_team else None,
                "price": player.price,
            },
            "seconds_remaining": seconds_remaining,
            "current_index": CURRENT_INDEX,
            "total_players": total_players,
            "user_expense_budget": user_expense_budget,
        }


def current_player_view(request):
    # ... your existing code ...
    logged_in_team_id = None
    if request.user.is_authenticated:
        try:
            logged_in_team_id = request.user.team.id
        except AttributeError:
            logged_in_team_id = None

    context = {
        'logged_in_team_id': logged_in_team_id,
        'user_role': getattr(request.user, 'role', '') if request.user.is_authenticated else '',
        'user_is_authenticated': request.user.is_authenticated,
        # other context variables...
    }
    return render(request, 'bidding/currentPlayer.html', context)


from django.views.decorators.cache import never_cache
@never_cache
def auction_status(request):
    info = get_current_player_info(request) # returns dict with player, status, etc.
    return JsonResponse(info)
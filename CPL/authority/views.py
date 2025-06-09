from django.shortcuts import render, redirect
from .forms import PlayerCategoryForm

from bidding.models import AuctionSettings
from django import forms



def dashboard(request):
    return render(request, 'authority/dashboard.html')



class AuctionSettingsForm(forms.ModelForm):
    class Meta:
        model = AuctionSettings
        fields = ['auction_start_time', 'player_duration']

# authority/views.py
from django.shortcuts import render, redirect
from django.utils.timezone import make_aware
from datetime import datetime, timedelta
from bidding.models import AuctionSettings
from django.utils.timezone import now

def set_auction_settings(request):
    # Fetch the single instance or create it
    settings, created = AuctionSettings.objects.get_or_create(id=1)

    if request.method == 'POST':
        start_time_str = request.POST.get('start_time')
        duration_seconds = request.POST.get('duration')

        try:
            dt = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
            settings.auction_start_time = make_aware(dt)
            settings.player_duration = timedelta(seconds=int(float(duration_seconds)))
            settings.save()
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

from django.db import models

# Create your models here.
from django.utils.timezone import now, timedelta

class AuctionSettings(models.Model):
    auction_start_time = models.DateTimeField(default=now)
    player_duration = models.DurationField(default=timedelta(seconds=20))

    
    player_default_duration = models.DurationField(default=timedelta(seconds=20))
    player_start_time = models.DateTimeField(default=now)
    player_current_index = models.IntegerField(default=0)
    auction_end_time = models.DateTimeField(default=now)
    auction_increase_time = models.DurationField(default=timedelta(seconds=10))
    
    def __str__(self):
        return "Auction Settings"
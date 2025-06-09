from django.db import models

# Create your models here.
from django.utils.timezone import now, timedelta

class AuctionSettings(models.Model):
    auction_start_time = models.DateTimeField(default=now)
    player_duration = models.DurationField(default=timedelta(seconds=20))

    def __str__(self):
        return "Auction Settings"
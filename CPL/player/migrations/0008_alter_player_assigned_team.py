# Generated by Django 5.1.6 on 2025-06-21 18:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0007_merge_0005_player_price_0006_player_player_class'),
        ('team', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='assigned_team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='players', to='team.team'),
        ),
    ]

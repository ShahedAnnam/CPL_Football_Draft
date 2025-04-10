# Generated by Django 5.1.4 on 2025-03-25 11:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('player', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlayerCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('A', 'Category A'), ('B', 'Category B'), ('C', 'Category C')], max_length=1)),
                ('base_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('assigned_at', models.DateTimeField(auto_now=True)),
                ('player', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='player.player')),
            ],
        ),
    ]

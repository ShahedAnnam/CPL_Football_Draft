from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import TeamProfile
from .forms import TeamProfileForm


def dashboard(request):
    return render(request, 'team/dashboard.html')



@login_required
def complete_profile(request):
    try:
        profile = request.user.teamprofile  # Get existing profile
        form = TeamProfileForm(request.POST or None, request.FILES or None, instance=profile)
    except TeamProfile.DoesNotExist:
        form = TeamProfileForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('team:dashboard')

    return render(request, 'team/complete_profile.html', {'form': form})




@login_required
def team_list(request):
    teams = TeamProfile.objects.all()
    return render(request, 'team/team_list.html', {'teams': teams})
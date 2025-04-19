from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import TeamProfile
from .forms import TeamProfileForm


def dashboard(request):
    return render(request, 'team/dashboard.html')



@login_required
def complete_profile(request):
    if hasattr(request.user, 'teamprofile'):
        return redirect('team:dashboard')  # Already completed

    if request.method == 'POST':
        form = TeamProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('team:dashboard')
    else:
        form = TeamProfileForm()

    return render(request, 'team/complete_profile.html', {'form': form})
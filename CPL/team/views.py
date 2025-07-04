from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Team
from .forms import TeamForm


def dashboard(request):
    return render(request, 'team/dashboard.html')



@login_required
def complete_profile(request):
    try:
        profile = request.user.team  # Get existing profile
        form = TeamForm(request.POST or None, request.FILES or None, instance=profile)
    except Team.DoesNotExist:
        form = TeamForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('team:dashboard')

    return render(request, 'team/complete_profile.html', {'form': form})




@login_required
def team_list(request):
    teams = Team.objects.all().prefetch_related('players')  # players from related_name in Player.assigned_team FK
    return render(request, 'team/team_list.html', {'teams': teams})

from django.http import JsonResponse, Http404
from .models import Team

def team_budget_view(request, team_id):
    try:
        team = Team.objects.get(id=team_id)
    except Team.DoesNotExist:
        raise Http404("Team not found")

    return JsonResponse({
        "team_id": team.id,
        "team_name": team.user.username,
        "expense_budget": team.expense_budget
    })
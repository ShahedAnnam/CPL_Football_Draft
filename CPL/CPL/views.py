from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from player.models import Player
from team.models import Team



def home(request):
    player_count = Player.objects.count()
    team_count = Team.objects.count()
    return render(request, 'cpl/home.html', {
        'player_count': player_count,
        'team_count': team_count
    })


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            if user.role == 'player':
                return redirect('player:dashboard')
            elif user.role == 'team':
                return redirect('team:dashboard')
            elif user.role == 'authority':
                return redirect('authority:dashboard')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'CPL/login.html')




def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Optional: auto login after registration
            return redirect('home')  # Change as needed
    else:
        form = CustomUserCreationForm()
    return render(request, 'CPL/register.html', {'form': form})


@login_required
def profile_view(request):
    password_form = PasswordChangeForm(request.user)

    if request.method == 'POST':
        if 'change_password' in request.POST:
            password_form = PasswordChangeForm(user=request.user, data=request.POST)
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, password_form.user)  # Keeps user logged in
                messages.success(request, 'Your password was changed successfully.')
                return redirect('profile')  # refresh the page
        elif 'logout' in request.POST:
            from django.contrib.auth import logout
            logout(request)
            request.session.flush()  # Clears any additional session data manually (if needed)
            return redirect('home')

    return render(request, 'CPL/profile.html', {
        'password_form': password_form
    })
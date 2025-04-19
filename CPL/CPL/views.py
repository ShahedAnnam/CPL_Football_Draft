from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import CustomUserCreationForm

def home(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            if user.role == 'player':
                return redirect('player:dashboard')
            elif user.role == 'team_owner':
                return redirect('team:dashboard')
            elif user.role == 'authority':
                return redirect('authority:dashboard')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'CPL/home.html')



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
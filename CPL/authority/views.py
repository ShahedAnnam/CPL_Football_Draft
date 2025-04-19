from django.shortcuts import render, redirect
from .forms import PlayerCategoryForm




def dashboard(request):
    return render(request, 'authority/dashboard.html')

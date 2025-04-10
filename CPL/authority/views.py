from django.shortcuts import render, redirect
from .forms import PlayerCategoryForm

def assign_category(request):
    if request.method == "POST":
        form = PlayerCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_success')  # Redirect to success page
    else:
        form = PlayerCategoryForm()
    
    return render(request, "authority/assign_category.html", {"form": form})

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def index(request):
    return render(request, 'index.html')


@login_required(login_url='/login/')  
def dashboard_view(request):
    return render(request, 'dashboard.html')


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")  
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")

def signup_page_view(request):
    return render(request, 'signup.html')


def logout_view(request):
    logout(request)  
    return redirect('/')

def patient_dashboard(request):
    return render(request, 'patient_dashboard.html')


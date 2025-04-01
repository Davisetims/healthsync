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

            # Redirect based on user type
            if user.user_type == "patient":
                return redirect("patient-dashboard")
            elif user.user_type == "doctor":  # Assuming "provider" means doctor
                return redirect("doctor-dashboard")
            elif user.is_superuser:
                return redirect("admin-dashboard")
            else:
                messages.error(request, "Unauthorized access")
                return redirect("index")  

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

def doctor_dashboard(request):
    return render(request, 'doctor_dashboard.html')

def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

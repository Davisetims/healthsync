from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.models import User, Reminder, VirtualMeeting
from django.http import JsonResponse
import json
from appointments.views import get_user_appointments
from medication.views import get_user_prescriptions
from .forms import PatientRegistrationForm, ReminderForm, VirtualMeetingForm,\
UserProfileForm


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

@login_required(login_url='/login/') 
def patient_dashboard(request):
    user = request.user
    _, total_appointments = get_user_appointments(user)
    response = get_user_prescriptions(request)  # This returns a JsonResponse
    response_data = json.loads(response.content)  # Convert JSON to Python dict
    total_prescriptions = response_data.get("total_prescriptions", 0)
    return render(request, 'patient_dashboard.html',
        {'total_appointments': total_appointments, 
        'total_prescriptions': total_prescriptions}
        )
                  

@login_required(login_url='/login/') 
def doctor_dashboard(request):
    user = request.user
    total_patients = User.objects.filter(user_type='patient').count() 
    _, total_appointments = get_user_appointments(user)
    response = get_user_prescriptions(request)  # This returns a JsonResponse
    response_data = json.loads(response.content)  # Convert JSON to Python dict
    total_prescriptions = response_data.get("total_prescriptions", 0)
    return render(
        request, 'doctor_dashboard.html',
        {'total_appointments': total_appointments,
        'total_patients': total_patients, 
        'total_prescriptions': total_prescriptions})
          

  

@login_required(login_url='/login/') 
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

from django.http import JsonResponse
from .models import User

@login_required(login_url='/login/') 
def user_list(request):
    user_type = request.GET.get('user_type')  # Get user_type from query parameters
    users = User.objects.all()

    if user_type:
        users = users.filter(user_type='patient')

    user_data = users.values("id", "email", "first_name", "last_name", "user_type", "country", "city")

    return render(request, 'patients.html', {"users": user_data})


def register_patient(request):
    if request.method == "POST":
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")  # Redirect to login or dashboard
    else:
        form = PatientRegistrationForm()
    
    return render(request, "signup.html", {"form": form})

@login_required(login_url='/login/') 
def send_reminder(request):
    if request.user.user_type != 'doctor':
        return redirect('index')  # Restrict access to only doctors

    if request.method == 'POST':
        form = ReminderForm(request.POST)
        if form.is_valid():
            reminder = form.save(commit=False)
            reminder.save()
            return redirect('doctor-dashboard')  # Redirect to the doctor's dashboard after saving
    else:
        form = ReminderForm()

    return render(request, 'send_reminder.html', {'form': form})

@login_required(login_url='/login/') 
def get_reminders_data(user):
    """Returns reminders and total reminders count for a given user"""
    if user.user_type in ['doctor', 'patient']:
        reminders = Reminder.objects.filter(user=user)
    else:
        reminders = Reminder.objects.none()

    total_reminders = reminders.count()  # Count total reminders
    return reminders, total_reminders


def reminders(request):
    """View to render patient's dashboard with reminders count"""
    user = request.user
    _, total_reminders = get_reminders_data(user)
    print(total_reminders)

    return render(request, 'patient_dashboard.html', {'total_reminders': total_reminders})


@login_required(login_url='/login/')
def create_virtual_meeting(request):
    if request.user.user_type != 'doctor':  
        return redirect('login')  # Redirect non-doctors

    if request.method == 'POST':
        form = VirtualMeetingForm(request.POST)
        if form.is_valid():
            meeting = form.save(commit=False)
            meeting.doctor = request.user  # Assign logged-in doctor
            meeting.save()
            return redirect('doctor-dashboard')  # Redirect to dashboard after saving
    else:
        form = VirtualMeetingForm()

    return render(request, 'meeting.html', {'form': form})


@login_required(login_url='/login/')
def get_virtual_meetings(request):
    user = request.user

    if user.user_type == 'doctor':
        meetings = VirtualMeeting.objects.filter(doctor=user)  # Doctor's meetings
    elif user.user_type == 'patient':
        meetings = VirtualMeeting.objects.filter(patient=user)  # Patient's meetings
    else:
        meetings = VirtualMeeting.objects.none()  # No meetings for other users

    return render(request, 'meeting_details.html', {'meetings': meetings})


@login_required(login_url='/login/')
def edit_profile(request):
    user = request.user  # Get logged-in user

    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            if user.user_type == 'doctor':
                return redirect('doctor-dashboard')  
            elif user.user_type == 'patient':
                return redirect('patient-dashboard')  
            else:
                return redirect('login') 

    else:
        form = UserProfileForm(instance=user)  # Pre-fill form with user data

    return render(request, 'edit_profile.html', {'form': form})
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from appointments.models import Appointment
from .forms import AppointmentForm

@login_required
def book_appointment(request):
    if request.user.user_type != "patient":
        messages.error(request, "Only patients can book appointments.")
        return redirect("index")  # Redirect non-patients

    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user  # Assign logged-in patient
            appointment.save()
            messages.success(request, "Appointment booked successfully!")
            return redirect("patient-dashboard")  # Redirect to appointments page
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = AppointmentForm()

    return render(request, "book_appointment.html", {"form": form})

@login_required
def user_appointments(request):
    user = request.user

    # Check if user is a patient or doctor and fetch relevant appointments
    if user.user_type == 'patient':
        appointments = Appointment.objects.filter(patient=user)
    elif user.user_type == 'doctor':
        appointments = Appointment.objects.filter(doctor=user)
    else:
        appointments = Appointment.objects.none()  # Return empty if not a patient or doctor

    return render(request, 'get_appointment.html', {'appointments': appointments})
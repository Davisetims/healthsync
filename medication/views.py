from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from medication.models import MedicalRecord, HealthProfile ,Prescription
from users.models import User
from .forms import PrescriptionForm


@login_required(login_url='/login/')  
def get_medical_records(request):
    if request.user.is_authenticated:
        try:
            health_profile = HealthProfile.objects.get(user=request.user)
            records = MedicalRecord.objects.filter(profile=health_profile).values(
                "condition", "diagnosis_date", "notes"
            )

            return JsonResponse({"records": list(records)})

        except HealthProfile.DoesNotExist:
            return JsonResponse({"error": "Health profile not found"}, status=404)

    return JsonResponse({"error": "Unauthorized"}, status=401)


@csrf_exempt
@login_required(login_url='/login/')
def post_prescription(request):
    if request.method == "POST":
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.prescribed_by = request.user  # The logged-in doctor
            prescription.save()
            return redirect("doctor-dashboard") 
        else:
            return JsonResponse({"error": form.errors}, status=400)

    else:
        form = PrescriptionForm()
        patients = User.objects.filter(user_type='patient')  # Only list patients
        return render(request, 'post_prescriptions.html', {'form': form, 'patients': patients})


@login_required(login_url='/login/')
def get_user_prescriptions(request):
    user = request.user

    if user.user_type == "doctor":
        prescriptions = Prescription.objects.filter(prescribed_by=user)  # Doctor's prescriptions
    elif user.user_type == "patient":
        prescriptions = Prescription.objects.filter(patient=user)  # Patient's prescriptions
    else:
        prescriptions = Prescription.objects.none()  # No prescriptions for other users

    total_prescriptions = prescriptions.count()  # Count total prescriptions

    # Convert prescriptions to JSON format
    prescription_data = [
        {
            "patient": p.patient.username,
            "name": p.name,
            "dosage": p.dosage,
            "frequency": p.frequency,
            "start_date": p.start_date.strftime("%Y-%m-%d"),
            "end_date": p.end_date.strftime("%Y-%m-%d") if p.end_date else None,
        }
        for p in prescriptions
    ]

    return JsonResponse({"total_prescriptions": total_prescriptions, "prescriptions": prescription_data}, safe=False)
    

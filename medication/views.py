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
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from medication.models import MedicalRecord, HealthProfile ,Prescription
from users.models import User


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
        try:
            data = json.loads(request.body)
            patient = User.objects.get(id=data["patient"])
            prescription = Prescription.objects.create(
                patient=patient,
                name=data["name"],
                dosage=data["dosage"],
                frequency=data["frequency"],
                start_date=data["start_date"],
                end_date=data.get("end_date"),
                prescribed_by=request.user  # The logged-in doctor
            )
            return JsonResponse({"message": "Prescription added successfully!"}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request"}, status=400)
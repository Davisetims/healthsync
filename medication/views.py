from django.shortcuts import render
from django.http import JsonResponse
from medication.models import MedicalRecord, HealthProfile
from django.contrib.auth.decorators import login_required

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

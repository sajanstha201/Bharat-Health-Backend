from rest_framework.permissions import BasePermission
from bharat_health.models import *
from rest_framework.exceptions import PermissionDenied
class IsDoctorPermitted(BasePermission):
    def has_permission(self, request, view):
        try:
            patient_id=request.query_params.get('patient_id')
            doctor_id=request.query_params.get('doctor_id')
            if not patient_id or not doctor_id:
                raise PermissionDenied("patient or doctor id not included")
            permission=PermissionPatientDoctor.objects.filter(patient=patient_id,doctor=doctor_id).first()
            if permission is None:
                raise PermissionDenied("invalid credientials")
            return permission.is_allowed
        except Exception as e:
            raise PermissionDenied(e)
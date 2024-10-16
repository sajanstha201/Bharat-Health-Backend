from rest_framework.permissions import BasePermission
from bharat_health.models import *
from rest_framework.exceptions import PermissionDenied
class IsDoctorPermitted(BasePermission):
    def has_permission(self, request, view):
        try:
            patient_id=request.query_params.get('patient_id')
            doctor_id=view.kwargs.get('pk')
            if not patient_id:
                raise PermissionDenied("patient id not included")
            if not doctor_id:
                raise PermissionDenied("doctor id not included")
            permission=PermissionPatientDoctor.objects.filter(patient=patient_id,doctor=doctor_id).first()
            if permission is None:
                raise PermissionDenied("invalid credientials")
            return permission.is_allowed
        except Exception as e:
            raise PermissionDenied(e)
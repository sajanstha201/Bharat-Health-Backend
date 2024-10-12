from bharat_health.models import *
from rest_framework import serializers
class MedicalReportSerializer(serializers.ModelSerializer):
    class Meta:
        model=MedicalPrescriptions
        fields='__all__'
        
        
class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Appointments
        fields='__all__'
        
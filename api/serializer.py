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
        
class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model=Patients
        exclude=['password']
        
class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Doctors
        exclude=['password']
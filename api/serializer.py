from bharat_health.models import *
from rest_framework import serializers
import uuid
from django.contrib.auth.hashers import make_password

class PatientToViewDoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Doctors
        fields=['doctor_id','first_name','last_name','middle_name','sex','phone_no','gmail','rating','specialization','profile_image']
        
class MedicalReportSerializer(serializers.ModelSerializer):
    doctor_detail=PatientToViewDoctorSerializer(source='doctor',read_only=True)
    class Meta:
        model=MedicalPrescriptions
        fields='__all__'
        extra_fields=['doctor_detail']
  
        
class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Appointments
        fields='__all__'
        
class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model=Patients
        exclude=['password']
    def create(self, validated_data):
        unique_token=str(uuid.uuid4())
        validated_data['token']=unique_token
        return super().create(validated_data)
    
class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Doctors
        exclude=['password']
    def create(self, validated_data):
        unique_token=str(uuid.uuid4())
        validated_data['token']=unique_token
        return super().create(validated_data)
    def update(self, instance, validated_data):
        validated_data.pop('token', None)   
        return super().update(instance, validated_data)    

class DoctorToViewPatientSerializer(serializers.ModelSerializer):
    class Meta:
        model=Patients
        fields=['first_name','middle_name','last_name','sex','age','phone_no','gmail','dob'] 
        
class PatientAppointmentWithDoctorDetailSerializer(serializers.ModelSerializer):
    doctor = PatientToViewDoctorSerializer(read_only=True)  # Include doctor details

    class Meta:
        model = Appointments
        fields = [
            'appointment_id',
            'appointment_date',
            'appointment_time',
            'appointment_type',
            'appointment_status',
            'created_at',
            'updated_at',
            'doctor'  # Added missing comma
        ]
class PatientMedicalReportWithDoctorDetailSerializer(serializers.ModelSerializer):
    doctor=PatientToViewDoctorSerializer(read_only=True)
    class Meta:
        model=MedicalPrescriptions
        fields="__all__"

class PermissionPatientDoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model=PermissionPatientDoctor
        fields="__all__"
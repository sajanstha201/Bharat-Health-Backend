from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from bharat_health.models import *
from rest_framework.decorators import authentication_classes,permission_classes
from rest_framework.exceptions import ValidationError,NotFound
from .serializer import *
from .authentication import *
from .permission import *

class DoctorViewset(viewsets.ModelViewSet):
    serializer_class = DoctorSerializer
    authentication_classes = [DoctorTokenAuthentication]

    def list(self, request, *args, **kwargs):
        return Response({'error': 'unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

    def get_object(self):
        if not self.kwargs.get('pk'):
            raise NotFound({'error': 'doctor id not found'})
        return super().get_object()

    def create(self, request):
        data = request.data
        serializer = self.get_serializer(data=data)
        if not serializer.is_valid():
            return Response({'error': 'invalid inputs'}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)  # Use HTTP_201_CREATED for successful creation

    def retrieve(self, request, *args, **kwargs):
        doctor_id = kwargs.get('pk')
        try:
            doctor = Doctors.objects.get(doctor_id=doctor_id)
            serializer = self.get_serializer(doctor)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Doctors.DoesNotExist:
            return Response({'error': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, *args, **kwargs):
        doctor_id = kwargs.get('pk')
        print(request.data)
        try:
            doctor = Doctors.objects.get(doctor_id=doctor_id)
            serializer = self.get_serializer(doctor, data=request.data, partial=True)
            if not serializer.is_valid():
                return Response({'error': 'not valid inputs'}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Doctors.DoesNotExist:
            return Response({'error': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)
        
class DoctorMedicalReportViewset(viewsets.ModelViewSet):
    queryset=MedicalPrescriptions.objects.all()
    serializer_class=MedicalReportSerializer
    authentication_classes=[DoctorTokenAuthentication]
    permission_classes=[IsDoctorPermitted]
    def list(self,request):
        try:
            patient_id=request.query_params.get('patient_id')
            if not patient_id:
                return Response({'error':'patient id not included'},status=status.HTTP_400_BAD_REQUEST)
            data=MedicalPrescriptions.objects.filter(patient=patient_id)
            serializer=MedicalReportSerializer(data,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response(e,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def create(self,request,*args,**kwargs):
        try:
            medical_report_serializer=self.get_serializer(data=request.data)
            if(medical_report_serializer.is_valid()):
                medical_report_serializer.save()
                return Response(medical_report_serializer.data,status=status.HTTP_200_OK)
            else:
                return Response({'error','invalid data'},status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response(error,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
class DoctorAppointmentViewset(viewsets.ModelViewSet):
    serializer_class=AppointmentSerializer
    authentication_classes=[DoctorTokenAuthentication]
    
    def get_queryset(self):
        doctor_id = self.kwargs.get('pk')
        if not doctor_id:
            raise NotFound({'error':'doctor id not found'})
        return Appointments.objects.filter(doctor_id=doctor_id)
    
    def get_object(self):
        doctor_id=self.kwargs.get('pk')
        if not doctor_id:
            raise NotFound({'error':'doctor id not found'})
        return super().get_object()
    
    def retrieve(self, request, *args, **kwargs):
        data=self.get_queryset()
        serializers=self.get_serializer(data,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)
    
    def partial_update(self, request, *args, **kwargs):
        appointment_id=request.data['appointment_id']
        if not appointment_id:
            return Response({'error':'appointent id not included'},status=status.HTTP_400_BAD_REQUEST)
        appointment=Appointments.objects.get(appointment_id=appointment_id)
        if not appointment:
            return Response({'error':'appointment does not exist'},status=status.HTTP_400_BAD_REQUEST)
        serializers=self.get_serializer(appointment,data=request.data,partial=True)
        if not serializers.is_valid():
            return Response({'error':'invalid inputs'},status=status.HTTP_400_BAD_REQUEST)
        serializers.save()
        return Response(serializers.data,status=status.HTTP_200_OK)
        
    def list(self,request):
        return Response({'error': 'not valid'}, status=status.HTTP_401_UNAUTHORIZED)
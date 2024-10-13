from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from bharat_health.models import *
from rest_framework.decorators import authentication_classes
from .serializer import *
from .authentication import *
from rest_framework.exceptions import NotFound
import uuid
from django.contrib.auth.hashers import make_password


class PatientViewset(viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    authentication_classes = [PatientTokenAuthentication]

    def list(self, request, *args, **kwargs):
        return Response({'error': 'unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

    def get_object(self, pk):
        try:
            return Patients.objects.get(patient_id=pk)
        except Patients.DoesNotExist:
            raise NotFound({'error': 'patient id not found'})
        
    @action(methods=['POST'],detail=False,url_path='create',authentication_classes=[])
    def createNewUser(self,request):
        data=request.data
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'error': 'invalid inputs', 'details': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    
    def create(self, request):
        # serializer = self.get_serializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'error':'not allowed'},status=status.HTTP_403_FORBIDDEN)

    def retrieve(self, request, *args, **kwargs):
        patient_id = kwargs.get('pk')
        patient = self.get_object(patient_id)
        serializer = self.get_serializer(patient)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        patient_id = kwargs.get('pk')
        patient = self.get_object(patient_id)

        serializer = self.get_serializer(patient, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error': 'not valid inputs', 'details': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    


class PatientToViewDoctorViewset(viewsets.ModelViewSet):
    serializer_class=PatientToViewDoctorSerializer
    queryset=Doctors.objects.all()
    
class PatientMedicalReportViewset(viewsets.ModelViewSet):
    serializer_class=MedicalReportSerializer
    authentication_classes=[PatientTokenAuthentication]
    
    def get_queryset(self):
        patient_id=self.kwargs.get('pk')
        return MedicalPrescriptions.objects.filter(patient_id=patient_id)
    
    def get_object(self):
        patient_id=self.kwargs.get('pk')
        if not patient_id:
            raise NotFound({'error':'patient id not included'})
        return super().get_object()
    
    def retrieve(self, request, *args, **kwargs):
        try:
            medical_report=self.get_queryset()
            medical_report_serializer=self.get_serializer(medical_report,many=True)
            return Response(medical_report_serializer.data,status=status.HTTP_200_OK)
        except Exception as error:
            return Response(error,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def destroy(self, request, *args, **kwargs):
        medical_prescription_id=request.data['prescription_id']
        if not medical_prescription_id:
            return Response({'error':'medical prescription id not included'},status=status.HTTP_400_BAD_REQUEST)
        medical_report=MedicalPrescriptions.objects.filter(prescription_id=medical_prescription_id)
        medical_report.delete()
        return Response({'success':'successfully deleted'},status=status.HTTP_200_OK)


class PatientAppointmentViewset(viewsets.ModelViewSet):
    serializer_class=AppointmentSerializer
    authentication_classes=[PatientTokenAuthentication]
    
    def post(self,request,*args,**kwargs):
        data=request.data
        serializers=self.get_serializer(data=data)
        if not serializers.is_valid():
            return Response({'error':'invalid inputs'},status=status.HTTP_400_BAD_REQUEST)
        serializers.save()
        return Response(serializers.data,status=status.HTTP_200_OK)
    
    def retrieve(self, request, *args, **kwargs):
        patient_id=kwargs.get('pk')
        if not patient_id:
            return Response({'error':'patient id not included'},status=status.HTTP_400_BAD_REQUEST)
        data=Appointments.objects.filter(patient_id=patient_id).order_by('appointment_date','appointment_time')
        if not data:
            Response({'detail':'no appointment'},status=status.HTTP_404_NOT_FOUND)
        serializers=PatientAppointmentWithDoctorDetailSerializer(data,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        appointment_id=kwargs.get('pk')
        if not appointment_id:
            return Response({'error':'appointment id not included'},status=status.HTTP_400_BAD_REQUEST)
        appointment=Appointments.objects.get(appointment_id=appointment_id)
        appointment.delete()
        return Response({'success':'successfully deleted'},status=status.HTTP_200_OK)
    
    def partial_update(self, request, *args, **kwargs):
        patient_id=kwargs.get('pk')
        if not patient_id:
            return Response({'error':'patient id not included'},status=status.HTTP_400_BAD_REQUEST)
        appointment_id=request.data['appointment_id']
        appointment=Appointments.objects.get(appointment_id=appointment_id)
        serializers=self.get_serializer(appointment,data=request.data,partial=True)
        if not serializers.is_valid():
            return Response({'error':'invalid update'},status=status.HTTP_400_BAD_REQUEST)
        serializers.save()
        return Response(serializers.data,status=status.HTTP_200_OK)
    
    def list(self, request, *args, **kwargs):
        return Response({'error':'not applicable'},status=status.HTTP_401_UNAUTHORIZED)
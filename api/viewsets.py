from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from bharat_health.models import *
from .serializer import *
from .authentication import *

class AppointmentViewset(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    
    @action(methods=['GET'], detail=False, url_path='patient',
            authentication_classes=[PatientTokenAuthentication])
    def getPatientAppointment(self, request):
        patient_id = request.query_params.get('patient_id')
        if not patient_id:
            return Response({'error': 'patient id not included'}, status=status.HTTP_400_BAD_REQUEST)
        data = Appointments.objects.filter(patient_id=patient_id)
        serializers = self.get_serializer(data, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)
    
    @action(methods=['POST'],detail=False,url_path='create',
            authentication_classes=[PatientTokenAuthentication])
    def makeAppointment(self,request):
        serializers=self.get_serializer(request.data)
        if not serializers.is_valid():
            return Response({'error':'invalid input'},status=status.HTTP_400_BAD_REQUEST)
        serializers.save()
        return Response(serializers.data,status=status.HTTP_200_OK)
    
    
    @action(methods=['GET'], detail=False, url_path='doctor')    
    def getDoctorAppointment(self, request):
        doctor_id = request.query_params.get('doctor_id')
        if not doctor_id:
            return Response({'error': 'doctor id not included'}, status=status.HTTP_400_BAD_REQUEST)
        data = Appointments.objects.filter(doctor_id=doctor_id)
        serializers = self.get_serializer(data, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)


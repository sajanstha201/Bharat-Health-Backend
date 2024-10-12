from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from bharat_health.models import *
from rest_framework.decorators import authentication_classes
from .serializer import *
from .authentication import *
from rest_framework.exceptions import NotFound
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

    def create(self,request):
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
        data=Appointments.objects.filter(patient_id=patient_id)
        serializers=self.get_serializer(data,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        patient_id=kwargs.get('pk')
        if not patient_id:
            return Response({'error':'patient id not included'},status=status.HTTP_400_BAD_REQUEST)
        appointment_id=request.data['appointment_id']
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
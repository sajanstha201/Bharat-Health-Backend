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
from django.utils import timezone
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
    
    @action(methods=['POST'],detail=False,url_path='create',authentication_classes=[])
    def createNewUser(self,request):
        data=request.data
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save(password=data['password'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'error': 'invalid inputs', 'details': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
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
    serializer_class=MedicalReportSerializer
    authentication_classes=[DoctorTokenAuthentication]
    permission_classes=[IsDoctorPermitted]
    def get_queryset(self):
        patient_id=self.request.query_params.get('patient_id')
        if not patient_id:
            return Response({'error':'patient id not included'},status=status.HTTP_400_BAD_REQUEST)
        return MedicalPrescriptions.objects.filter(patient_id=patient_id)
    
    def retrieve(self,request,*args,**kwargs):
        try:
            patient_id=request.query_params.get('patient_id')
            if not patient_id:
                return Response({'error':'patient id not included'},status=status.HTTP_400_BAD_REQUEST)
            data=MedicalPrescriptions.objects.filter(patient=patient_id)
            serializer=MedicalReportSerializer(data,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response(e,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self,request,*args,**kwargs):
        try:
            print('creating a new user')
            print(request.data)
            medical_report_serializer=MedicalReportSerializer(data=request.data)
            if(medical_report_serializer.is_valid()):
                medical_report_serializer.save()
                return Response(medical_report_serializer.data,status=status.HTTP_200_OK)
            else:
                return Response({'error','invalid data'},status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response(error,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def list(self, request, *args, **kwargs):
        return Response({'error':'unauthorized access'},status=status.HTTP_403_FORBIDDEN)
        
        
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
        doctor_id=self.kwargs.get('pk')
        appointment_status=request.query_params.get('status')
        today_date=timezone.now().date()
        if appointment_status=='completed':
            data=Appointments.objects.filter(doctor_id=doctor_id,appointment_status='completed').order_by('appointment_date','appointment_time')
        elif appointment_status=='upcomming':
            data=Appointments.objects.filter(doctor_id=doctor_id).exclude(appointment_status='completed').order_by('appointment_date','appointment_time')
        elif appointment_status=='today':
            data=Appointments.objects.filter(doctor_id=doctor_id,appointment_date=today_date)
        else:
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
    
class DoctorToViewPatientViewset(viewsets.ModelViewSet):
    serializer_class=DoctorToViewPatientSerializer
    authentication_classes=[DoctorTokenAuthentication]
    def list(self, request, *args, **kwargs):
        return Response({'error':'unauthorized'},status=status.HTTP_401_UNAUTHORIZED)
    def retrieve(self, request, *args, **kwargs):
        patient_id=kwargs.get('pk')
        data=Patients.objects.filter(patient_id=patient_id)
        if not data:
            return Response({'error':'not found'},status=status.HTTP_404_NOT_FOUND)
        serializers=DoctorToViewPatientSerializer(data,many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)
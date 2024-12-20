from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action,api_view,authentication_classes
from rest_framework import status
from bharat_health.models import *
from .serializer import *
from .authentication import *
from django.contrib.auth.hashers import make_password,check_password
from disease_prediction.main import get_keywords

@api_view(['GET'])
def getUserInfo(request):
    if(request.method=='GET'):
        token=request.headers['Authorization'].split(' ')[1]
        print(token)
        patient=Patients.objects.filter(token=token).first()
        doctor=Doctors.objects.filter(token=token).first()
        if patient:
            serializers=PatientSerializer(patient)
        elif doctor:
            print('doctor selectd')
            serializers=DoctorSerializer(doctor)
        else:
            print("none selected")
            Response({'error':'invalid token'},status=status.HTTP_404_NOT_FOUND)
        return Response(serializers.data,status=status.HTTP_200_OK)
    else:
        return Response({'error':'not  a get method'},status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['POST'])  # Change to POST request
def loginUser(request):
    try:
        data = request.data
        password=data['password']
        patient = Patients.objects.filter(gmail=data['email']).first()
        doctor = Doctors.objects.filter(gmail=data['email']).first()
        if patient and password== patient.password:
            serializer = PatientSerializer(patient)
        elif doctor and password== doctor.password:
            serializer = DoctorSerializer(doctor) 
        else:
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        print('Error occurred during login:', e)
        return Response({'error': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
@authentication_classes([DoctorTokenAuthentication])
def predictDisease(request):
    print(request.data)
    d=request.data['data']
    key_words=get_keywords(d)
    return Response({'keywords':key_words},status=status.HTTP_200_OK)
        
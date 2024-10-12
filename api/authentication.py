from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from bharat_health.models import *
class PatientTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        try:
            authentication_token=request.headers['Authorization'].split(' ')[1]
            if not authentication_token:
                raise AuthenticationFailed("Token not included")
            object=Patients.objects.get(token=authentication_token)
        except Exception as e:
            raise AuthenticationFailed("Invalid Token")
        return (object,None)
        
        
class DoctorTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        try:
            token=request.headers.get('Authorization').split(' ')[1]
            if not token:
                return AuthenticationFailed("Token not included")
            object=Doctors.objects.get(token=token)
        except Exception as e:
            raise AuthenticationFailed("Invalid Token")
        return (object,None)
        
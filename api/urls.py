from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .patient_viewset import *
from .doctor_viewset import *
from .viewsets import *

patient_router = DefaultRouter()
patient_router.register(r'medical-report', PatientMedicalReportViewset, basename='medical-report')
patient_router.register(r'appointments', PatientAppointmentViewset, basename='patient-appointment')
patient_router.register(r'profile',PatientViewset,basename='profile')
patient_router.register(r'view-doctors',PatientToViewDoctorViewset,basename='view-doctors')


doctor_router = DefaultRouter()
doctor_router.register(r'medical-report', DoctorMedicalReportViewset, basename='medical-report')
doctor_router.register(r'appointments', DoctorAppointmentViewset, basename='doctor-appointment')
doctor_router.register(r'profile',DoctorViewset,basename='profile')


router = DefaultRouter()
router.register(r'appointments', AppointmentViewset, basename='appointment')

urlpatterns = [
    path('patient/', include(patient_router.urls)),
    path('doctor/', include(doctor_router.urls)),
    path('', include(router.urls)),
]

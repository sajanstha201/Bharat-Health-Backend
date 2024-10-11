from rest_framework.routers import DefaultRouter
from .viewset import *
from django.urls import path,include
router=DefaultRouter()
router.register(r'medical-report',MedicalReportViewset,basename='medical')
urlpatterns = [
    path('',include(router.urls))
]

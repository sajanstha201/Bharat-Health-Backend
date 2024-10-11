from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
class MedicalReportViewset(viewsets.ModelViewSet):
    @action(methods=['GET'],url_path='g',detail=False)
    def getMedicalReport(self,request):
        return Response({'name':'sajan shrestha'})
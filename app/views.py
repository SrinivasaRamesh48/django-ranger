from django.http import HttpResponse
from rest_framework import viewsets
from .models.BulkEmailTemplate import BulkEmailTemplate
from .models.BulkEmailTemplate import BulkMessageType
from .models.BulkPhoneTemplate import BulkPhoneTemplate
from .models.CPEControlLog import CPEControlLog
from .models.CPEControlLogType import CPEControlLogType
from .serializers.builk_serializers import BulkEmailTemplateSerializer
from .serializers.builk_serializers import BulkMessageTypeSerializer
from .serializers.builk_serializers import BulkPhoneTemplateSerializer
from .serializers.CPEControlLogSerializer import CPEControlLogSerializer
from .serializers.CPEControlLogSerializer import CPEControlLogTypeSerializer

class BulkEmailTemplateViewSet(viewsets.ModelViewSet):
    queryset = BulkEmailTemplate.objects.all()
    serializer_class = BulkEmailTemplateSerializer

class BulkMessageTypeViewSet(viewsets.ModelViewSet):
    queryset = BulkMessageType.objects.all()
    serializer_class = BulkMessageTypeSerializer

class BulkPhoneTemplateViewSet(viewsets.ModelViewSet):
    queryset = BulkPhoneTemplate.objects.all()
    serializer_class = BulkPhoneTemplateSerializer

class CPEControlLogViewSet(viewsets.ModelViewSet):
    queryset = CPEControlLog.objects.all()
    serializer_class = CPEControlLogSerializer

class CPEControlLogTypeViewSet(viewsets.ModelViewSet):
    queryset = CPEControlLogType.objects.all()
    serializer_class = CPEControlLogTypeSerializer
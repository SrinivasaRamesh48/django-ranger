from django.http import HttpResponse
from rest_framework import viewsets
from .models.BulkEmailTemplate import BulkEmailTemplate
from .models.BulkEmailTemplate import BulkMessageType
from .models.BulkPhoneTemplate import BulkPhoneTemplate
from .serializers.builk_serializers import BulkEmailTemplateSerializer
from .serializers.builk_serializers import BulkMessageTypeSerializer
from .serializers.builk_serializers import BulkPhoneTemplateSerializer


class BulkEmailTemplateViewSet(viewsets.ModelViewSet):
    queryset = BulkEmailTemplate.objects.all()
    serializer_class = BulkEmailTemplateSerializer

class BulkMessageTypeViewSet(viewsets.ModelViewSet):
    queryset = BulkMessageType.objects.all()
    serializer_class = BulkMessageTypeSerializer

class BulkPhoneTemplateViewSet(viewsets.ModelViewSet):
    queryset = BulkPhoneTemplate.objects.all()
    serializer_class = BulkPhoneTemplateSerializer
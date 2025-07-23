from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from app.serializers.user_company_serializer import UserCompanySerializer
from app.models import UserCompany

class UserCompanyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UserCompany.objects.all()
    serializer_class = UserCompanySerializer
    permission_classes = [IsAuthenticated]
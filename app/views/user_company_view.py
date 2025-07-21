from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from app.serializers.user_company_serializer import UserCompanySerializer
from app.models import UserCompany
# from .models import UserCompany
# from .serializers import UserCompanySerializer

class UserCompanyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A read-only ViewSet for retrieving User Companies.
    - GET /user_companies -> Triggers the `list` action.
    """
    # The queryset defines the data to be returned.
    # The default ordering is already set in the model's Meta class.
    queryset = UserCompany.objects.all()
    serializer_class = UserCompanySerializer
    permission_classes = [IsAuthenticated]
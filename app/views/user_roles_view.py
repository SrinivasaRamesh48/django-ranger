from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from app.serializers import UserRolesSerializer
from app.models import UserRoles
# from .models import UserRoles
# from .serializers import UserRolesSerializer

class UserRolesViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A read-only ViewSet for retrieving User Roles.
    - GET /user_roles -> Triggers the `list` action.
    """
    # The queryset defines the data to be returned.
    # The default ordering is already set in the model's Meta class.
    queryset = UserRoles.objects.all()
    serializer_class = UserRolesSerializer
    permission_classes = [IsAuthenticated]
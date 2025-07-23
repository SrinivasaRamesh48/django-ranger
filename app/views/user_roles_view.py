from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from app.serializers.user_roles_serializer import UserRolesSerializer
from app.models import UserRoles

class UserRolesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UserRoles.objects.all()
    serializer_class = UserRolesSerializer
    permission_classes = [IsAuthenticated]
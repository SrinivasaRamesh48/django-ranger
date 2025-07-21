from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from app.models.builder import Builder
from app.serializers.builder_serializer import BuilderSerializer

class BuilderViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A read-only ViewSet for retrieving builders.
    This corresponds to `BuildersController@index`.
    - GET /builders -> Triggers the `list` action.
    """
    queryset = Builder.objects.all()
    serializer_class = BuilderSerializer
    permission_classes = [IsAuthenticated]
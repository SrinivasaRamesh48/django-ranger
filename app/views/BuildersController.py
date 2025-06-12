from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from app.models.Builder import Builder
from app.serializers.BuilderSerializer import BuilderSerializer

class BuilderViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A read-only ViewSet for retrieving builders.
    This corresponds to `BuildersController@index`.
    - GET /builders -> Triggers the `list` action.
    """
    # The queryset defines the data to be returned.
    # The default ordering is already set in the model's Meta class.
    queryset = Builder.objects.all()
    serializer_class = BuilderSerializer
    permission_classes = [IsAuthenticated]
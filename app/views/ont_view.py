from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from app.models import Ont
from app.serializers import OntSerializer

class OntViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A read-only ViewSet for retrieving ONTs.
    This corresponds to `ONTController@index`.
    - GET /onts/ -> Triggers the `list` action.
    """
    # The queryset defines the data to be returned.
    # select_related is the Django equivalent of eager loading (`with`).
    queryset = Ont.objects.select_related('home', 'node', 'manufacturer').all()
    serializer_class = OntSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        """
        Overrides the default list action to provide a custom response format
        that matches the original Laravel API.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        
        response_data = {
            'success': True if data else False,
            'data': data,
            'message': 'Data Successfully Retrieved.' if data else 'Failed to Retrieve Data.'
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
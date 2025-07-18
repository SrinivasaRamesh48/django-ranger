from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from app.models import PortMacAddress
from app.serializers import PortMacAddressSerializer


class PortMacAddressViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A read-only ViewSet for viewing Port MAC Addresses.
    Corresponds to `PortMacAddressController@index`.
    """
    # Eager load related data for efficiency. The `__` traverses relationships.
    queryset = PortMacAddress.objects.select_related(
        'node', 'mac_address_found', 'mac_address_found__home'
    ).all()
    
    serializer_class = PortMacAddressSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        """
        Overrides the default list action to provide a custom response format.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        
        return Response({
            'success': True if data else False,
            'data': data,
            'message': 'Data Successfully Retrieved.' if data else 'Failed to Retrieve Data.'
        }, status=status.HTTP_200_OK)
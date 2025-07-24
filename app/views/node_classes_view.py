from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from app.models.node_class import NodeClass
from app.serializers.node_class_serializer import NodeClassSerializer



class NodeClassViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = NodeClass.objects.all()
    serializer_class = NodeClassSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        
        response_data = {
            'success': True if data else False,
            'data': data,
            'message': 'Data Successfully Retrieved.' if data else 'Failed to Retrieve Data.'
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
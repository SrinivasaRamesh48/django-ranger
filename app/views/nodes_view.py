from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from app.models.node import Node
from app.serializers.node_serializer import NodeSerializer

class NodeViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and managing Nodes (Equipment).
    """
    queryset = Node.objects.all()
    serializer_class = NodeSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'node_id'

    def get_queryset(self):
        """
        Eager loads related data to improve performance, equivalent to `with()`
        in Laravel.
        """
        return Node.objects.select_related(
            'node_frame', 'node_type', 'node_class', 'project'
        ).prefetch_related('homes', 'homes__subscribers')

    def list(self, request, *args, **kwargs):
        """Corresponds to the `index` method."""
        # Filter for active nodes and apply default ordering by hostname.
        queryset = self.get_queryset().filter(active=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'success': True,
            'data': serializer.data,
            'message': 'Data Successfully Retrieved.'
        })

    def retrieve(self, request, *args, **kwargs):
        """Corresponds to the `show` method."""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'success': True,
            'data': serializer.data,
            'message': 'Node Successfully Retrieved.'
        })

    def create(self, request, *args, **kwargs):
        """Corresponds to the `store` method."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            'success': True,
            'data': serializer.data,
            'message': 'Equipment Successfully Added.'
        }, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """Corresponds to the `update` method."""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            'success': True,
            'data': True, # Matching Laravel's response
            'message': 'Node Successfully Updated.'
        })

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from app.models.node_frame import NodeFrame
from app.serializers import NodeFrameSerializer
class NodeFrameViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A read-only ViewSet for retrieving Node Frames.
    This corresponds to `NodeFramesController@index`.
    - GET /node_frames -> Triggers the `list` action.
    """
    queryset = NodeFrame.objects.all()
    serializer_class = NodeFrameSerializer
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
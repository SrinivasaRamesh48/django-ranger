from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

from app.models import Circuit
from app.serializers import CircuitSerializer,UploadSerializer

class CircuitViewSet(viewsets.ModelViewSet):
    queryset = Circuit.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CircuitSerializer
        if self.action == 'upload_file':
            return UploadSerializer
        return CircuitSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().select_related('circuit_carrier', 'state')
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'success': True,
            'data': serializer.data,
            'message': 'Circuits Successfully Retrieved.'
        })

    @action(detail=False, methods=['get'], url_path='circuits-full')
    def circuits_full(self, request):
        queryset = Circuit.objects.select_related('circuit_carrier', 'state').order_by('title')
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'success': True,
            'data': serializer.data,
            'message': 'Circuits Successfully Retrieved.'
        })

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'success': True,
            'data': serializer.data,
            'message': 'Circuit Successfully Retrieved.'
        })

    @action(
        detail=True,
        methods=['post'],
        url_path='upload-circuit-file',
        parser_classes=[MultiPartParser, FormParser] # Important for file uploads
    )
    def upload_file(self, request, pk=None):
        circuit = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save(circuit=circuit)
            return Response({
                'success': True,
                'data': serializer.data,
                'message': 'File Successfully Uploaded.'
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'success': False,
                'errors': serializer.errors,
                'message': 'Failed to Upload File.'
            }, status=status.HTTP_400_BAD_REQUEST)
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from app.models import Project, Uploads
from app.serializers import (
 NodeSerializer,ProjectSerializer
)


class ProjectViewSet(viewsets.ModelViewSet):
    """
    A unified ViewSet for managing Projects. Corresponds to ProjectController.
    """
    queryset = Project.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'project_id'

    def get_serializer_class(self):
        return ProjectSerializer
        

    def get_queryset(self):
        """Eager load common relationships to improve performance."""
        return Project.objects.select_related(
            'us_state', 'builder', 'subscription_type', 'network_type', 'circuit'
        ).prefetch_related('homes', 'nodes', 'alerts')

    def list(self, request, *args, **kwargs):
        """Corresponds to the `index` method."""
        queryset = self.get_queryset().order_by('-circuit_id')
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'success': True, 'data': serializer.data, 'message': 'Projects Successfully Retrieved.'
        })

    @action(detail=False, methods=['get'], url_path='projects-full')
    def projects_full(self, request):
        """Corresponds to the `projects_full` method."""
        queryset = self.get_queryset() # Uses the base eager-loading
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'success': True, 'data': serializer.data, 'message': 'Projects Successfully Retrieved.'
        })

    def retrieve(self, request, *args, **kwargs):
        """Corresponds to the `show` method with custom data aggregation."""
        project = self.get_object() # This will use the queryset and lookup_field
        
        # --- Aggregate Alerts ---
        alerts_full = list(project.alerts.all())
        if project.circuit:
            alerts_full.extend(project.circuit.alerts.all())
        alerts_full.sort(key=lambda x: x.alert_type_id, reverse=True)
        
        # --- Group Nodes by Frame ---
        node_frames_map = {}
        for node in project.nodes.filter(active=True).select_related('node_frame'):
            frame_id = node.node_frame.id if node.node_frame else 0
            if frame_id not in node_frames_map:
                node_frames_map[frame_id] = {
                    "node_frame_id": frame_id,
                    "description": node.node_frame.description if node.node_frame else "Unassigned",
                    "nodes": []
                }
            node_frames_map[frame_id]["nodes"].append(NodeSerializer(node).data)
        
        # Add the custom aggregated data to the instance before serializing
        project.alerts_full = alerts_full
        project.node_frames = list(node_frames_map.values())
        
        serializer = self.get_serializer(project)
        return Response({
            'success': True, 'data': serializer.data, 'message': 'Project Successfully Retrieved.'
        })
        
    def perform_create(self, serializer):
        """Handle date formatting before saving."""
        activation_date = self.request.data.get('activation_date')
        if activation_date:
            # Assumes date is in a format Python can parse, e.g., YYYY-MM-DD
            serializer.validated_data['activation_date'] = activation_date
        serializer.save()

    # create() and update() are handled by ModelViewSet, but perform_create/update
    # can be used to inject logic.

    @action(detail=True, methods=['post'], parser_classes=[MultiPartParser, FormParser], url_path='upload-project-file')
    def upload_file(self, request, project_id=None):
        """Corresponds to the `upload_file` method."""
        project = self.get_object()
        file_obj = request.FILES.get('file')
        
        if not file_obj:
            return Response({'success': False, 'message': 'No file provided.'}, status=status.HTTP_400_BAD_REQUEST)
        
        upload = Uploads.objects.create(
            project=project,
            upload_type_id=2, # Corresponds to project docs
            name=request.data.get('name', 'Untitled'),
            path=file_obj
        )
        
        serializer = FileUploadSerializer(upload)
        return Response({
            'success': True, 'data': serializer.data, 'message': 'File Successfully Uploaded.'
        }, status=status.HTTP_201_CREATED)

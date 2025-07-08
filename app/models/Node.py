from django.db import models
from .node_frame import NodeFrame
from .node_class import NodeClass
from .node_type import NodeType
from .project import Project
from .time_stamped_model_mixin import TimeStampedModelMixin

class Node(TimeStampedModelMixin, models.Model):
    """Django equivalent of the Laravel Node model."""
    node_id = models.AutoField(primary_key=True)
    hostname = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField()
    mac_address = models.CharField(max_length=17)
    serial_number = models.CharField(max_length=100, blank=True, null=True)
    dns_ip_address = models.GenericIPAddressField(blank=True, null=True)
    active = models.IntegerField(default=1, blank=False, null=False)
    # Relationships
    node_frame = models.ForeignKey(NodeFrame, on_delete=models.CASCADE, db_column='node_frame_id')
    node_class = models.ForeignKey(NodeClass, on_delete=models.CASCADE, db_column='node_class_id')
    node_type = models.ForeignKey(NodeType, on_delete=models.CASCADE, db_column='node_type_id')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, db_column='project_id')

  
    class Meta:
        db_table = 'nodes'
    def __str__(self):
        return self.hostname
    
     
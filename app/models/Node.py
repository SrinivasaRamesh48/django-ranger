from django.db import models
# check once before migrating
class Node(models.Model):
    node_id = models.AutoField(primary_key=True)
    node_frame = models.ForeignKey('NodeFrame', on_delete=models.SET_NULL, null=True, blank=True, db_column='node_frame_id', related_name='nodes')
    node_type = models.ForeignKey('NodeType', on_delete=models.SET_NULL, null=True, blank=True, db_column='node_type_id', related_name='nodes')
    node_class = models.ForeignKey('NodeClass', on_delete=models.SET_NULL, null=True, blank=True, db_column='node_class_id', related_name='nodes')
    project = models.ForeignKey('Project', on_delete=models.SET_NULL, null=True, blank=True, db_column='project_id', related_name='nodes')
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    mac_address = models.CharField(max_length=255, blank=True, null=True)
    hostname = models.CharField(max_length=255, blank=True, null=True)
    serial_number = models.CharField(max_length=255, blank=True, null=True)
    dns_ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'nodes'
        app_label = 'app'

    def __str__(self):
        return self.hostname or f"Node {self.node_id}"
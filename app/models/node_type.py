from django.db import models

class NodeType(models.Model):
    node_type_id = models.AutoField(primary_key=True)


    class Meta:
        db_table = 'node_types'
        app_label = 'app'

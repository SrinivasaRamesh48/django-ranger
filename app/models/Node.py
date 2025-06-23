from django.db import models
from .node_frame import NodeFrame
from .node_class import NodeClass
from .node_type import NodeType
from .project import Project
# -*- coding: utf-8 -*-
class Node(models.Model):
    """Django equivalent of the Laravel Node model."""
    node_id = models.AutoField(primary_key=True)
    hostname = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField()
    mac_address = models.CharField(max_length=17)
    serial_number = models.CharField(max_length=100, blank=True, null=True)
    dns_ip_address = models.GenericIPAddressField(blank=True, null=True)

    # Relationships
    node_frame = models.ForeignKey(NodeFrame, on_delete=models.CASCADE, db_column='node_frame_id')
    node_class = models.ForeignKey(NodeClass, on_delete=models.CASCADE, db_column='node_class_id')
    node_type = models.ForeignKey(NodeType, on_delete=models.CASCADE, db_column='node_type_id')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, db_column='project_id')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'nodes'
    def __str__(self):
        return self.hostname
    
    
"""DROP TABLE IF EXISTS `nodes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `nodes` (
  `node_id` int(11) NOT NULL AUTO_INCREMENT,
  `node_frame_id` int(11) DEFAULT NULL,
  `node_class_id` int(11) NOT NULL,
  `node_type_id` int(11) DEFAULT NULL,
  `project_id` int(11) NOT NULL,
  `ip_address` varchar(255) DEFAULT NULL,
  `reg_ip_address` varchar(255) DEFAULT NULL,
  `mac_address` varchar(255) DEFAULT NULL,
  `hostname` varchar(255) DEFAULT NULL,
  `serial_number` varchar(255) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NULL DEFAULT NULL,
  `active` tinyint(1) NOT NULL DEFAULT 1,
  `dns_ip_address` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`node_id`),
  KEY `node_frame_id` (`node_frame_id`),
  KEY `node_class_id` (`node_class_id`),
  KEY `node_type_id` (`node_type_id`),
  KEY `project_id` (`project_id`)
) ENGINE=InnoDB AUTO_INCREMENT=90 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;   """    
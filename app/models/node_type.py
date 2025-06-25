from django.db import models

class NodeType(models.Model):
    node_type_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True, blank=False)
    class Meta:
        db_table = 'node_types'
        app_label = 'app'


""""
DROP TABLE IF EXISTS `node_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `node_types` (
  `node_type_id` int(11) NOT NULL AUTO_INCREMENT,
  `description` varchar(255) NOT NULL,
  `max_ports` int(11) DEFAULT NULL,
  `subscriber_switch` int(11) NOT NULL DEFAULT 0,
  `speed` int(11) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`node_type_id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

"""
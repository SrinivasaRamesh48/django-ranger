from django.db import models
from .BulkMessageType import BulkMessageType

class BulkEmailTemplate(models.Model):
    bulk_email_template_id = models.AutoField(primary_key=True)
    description = models.TextField()
    bulk_message_type = models.ForeignKey(BulkMessageType, on_delete=models.CASCADE, db_column='bulk_message_type_id')
    subject = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'bulk_email_templates'
        app_label = 'app'  

    def __str__(self):
        return f"Template: {self.subject}" 

    # SQL for creating the table
    
#     DROP TABLE IF EXISTS `bulk_email_templates`;
# /*!40101 SET @saved_cs_client     = @@character_set_client */;
# /*!40101 SET character_set_client = utf8 */;
# CREATE TABLE `bulk_email_templates` (
#   `outage_email_template_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
#   `bulk_message_type_id` int(11) DEFAULT NULL,
#   `description` varchar(255) NOT NULL DEFAULT '',
#   `subject` varchar(999) NOT NULL DEFAULT '',
#   `body` text NOT NULL,
#   `active` int(1) NOT NULL DEFAULT 1,
#   `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
#   `updated_at` timestamp NULL DEFAULT NULL ON UPDATE current_timestamp(),
#   PRIMARY KEY (`outage_email_template_id`),
#   KEY `bulk_message_type_id` (`bulk_message_type_id`)
# ) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
# /*!40101 SET character_set_client = @saved_cs_client */
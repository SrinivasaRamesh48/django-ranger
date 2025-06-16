from django.db import models
from .BulkMessageType import BulkMessageType
from .TimeStampedModelMixin import TimeStampedModelMixin


class BulkPhoneTemplate(TimeStampedModelMixin,models.Model):
    outage_phone_template_id = models.AutoField(primary_key=True)
    description = models.TextField(blank=True, null=True)
    body = models.TextField()
    active = models.BooleanField(default=True)
    message_type = models.ForeignKey(
        BulkMessageType,
        on_delete=models.SET_NULL,
        db_column='bulk_message_type_id',
        null=True,
        blank=True
    )

    class Meta:
        db_table = "bulk_phone_templates"

    def __str__(self):
        return f"Phone Template {self.bulk_phone_template_id} ({self.message_type.name})"
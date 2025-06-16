from django.db import models
from .ReportType import ReportType # Import the ReportType model

class SavedReport(models.Model):
    """Django equivalent of the Laravel SavedReport model."""
    saved_report_id = models.AutoField(primary_key=True)
    report_type = models.ForeignKey(ReportType, on_delete=models.CASCADE, related_name='saved_reports', db_column='report_type_id')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    data = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'saved_reports'
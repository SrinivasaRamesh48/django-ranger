from django.db import models
from .ReportType import ReportType # Import the ReportType model

class SavedReport(models.Model):
    saved_report_id = models.AutoField(primary_key=True)
    report_type = models.ForeignKey(
        ReportType,
        on_delete=models.CASCADE, # Assuming deleting a report type cascades to its saved reports
        db_column='report_type_id',
        related_name='saved_reports'
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    # Assuming 'data' field stores JSON. Use TextField if it's just plain text/serialized string.
    data = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'saved_reports'
        app_label = 'app'

    def __str__(self):
        return f"Saved Report {self.saved_report_id} - {self.title}"
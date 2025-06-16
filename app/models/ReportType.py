from django.db import models

class ReportType(models.Model):
    """Django equivalent of the Laravel ReportType model."""
    report_type_id = models.AutoField(primary_key=True)
    
    class Meta:
        db_table = "report_types"
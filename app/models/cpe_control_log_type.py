from django.db import models

class CPEControlLogType(models.Model):
    cpe_control_log_type_id = models.AutoField(primary_key=True)


    class Meta:
        db_table = 'cpe_control_log_types'
        app_label = 'app'

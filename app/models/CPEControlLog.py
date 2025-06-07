from django.db import models
from .CPEControlLogType import CPEControlLogType 
from .User import User

class CPEControlLog(models.Model):
    cpe_control_log_id = models.AutoField(primary_key=True)
    cpe_control_log_type = models.ForeignKey(CPEControlLogType, on_delete=models.CASCADE, db_column='cpe_control_log_type_id', related_name='cpe_control_logs'),
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='user_id', related_name='cpe_control_logs')
    canceled_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='canceled_by', related_name='canceled_cpe_control_logs')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cpe_control_log'
        app_label = 'app'

    def __str__(self):
        return f'CPE Control Log {self.cpe_control_log_id}'

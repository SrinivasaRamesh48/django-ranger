from django.db import models
from .cpe_control_log_type import CPEControlLogType 
from .user import User
from .time_stamped_model_mixin import TimeStampedModelMixin


class CPEControlLog(TimeStampedModelMixin, models.Model):
    cpe_control_log_id = models.AutoField(primary_key=True)
    log_type = models.ForeignKey(CPEControlLogType, on_delete=models.CASCADE, db_column='cpe_control_log_type_id')
    user_id = models.ForeignKey(User, related_name='cpe_control_logs', on_delete=models.CASCADE, db_column='user_id')
    canceled_by = models.ForeignKey(
        User, 
        related_name='canceled_cpe_control_logs', 
        on_delete=models.SET_NULL,
        null=True, 
        blank=True, 
        db_column='canceled_by'
    )
    class Meta:
        db_table = "cpe_control_log"
        

    def __str__(self):
        return f"Log {self.cpe_control_log_id} by {self.user_id.username} of type {self.log_type.name}"

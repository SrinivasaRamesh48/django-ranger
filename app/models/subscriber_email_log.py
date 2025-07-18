
from django.db import models
from app.models.time_stamped_model_mixin import TimeStampedModelMixin
class SubscriberEmailLog(TimeStampedModelMixin, models.Model):
    subscriber_email_log_id = models.AutoField(primary_key=True)
    sent_to = models.CharField(max_length=555,default='')
    success = models.IntegerField(default=0)

    # Relationships
    item = models.ForeignKey('EmailLogItem', on_delete=models.CASCADE, db_column='email_log_item_id')
    subscriber = models.ForeignKey('Subscriber', on_delete=models.CASCADE, db_column='subscriber_id')


    class Meta:
        db_table = 'subscriber_email_log'
        ordering = ['-created_at']
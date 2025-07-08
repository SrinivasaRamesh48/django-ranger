
from django.db import models
from .time_stamped_model_mixin import TimeStampedModelMixin


class StatementItem(TimeStampedModelMixin, models.Model):
    statement_item_id = models.AutoField(primary_key=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    custom = models.IntegerField(null=True, blank=True, default=0)

    # Relationships
    statement = models.ForeignKey('Statement', on_delete=models.CASCADE, related_name='items', db_column='statement_id')
    description = models.ForeignKey("StatementItemDescription", on_delete=models.PROTECT, db_column='statement_item_description_id')
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, null=True, blank=True, db_column='payment_id')

    class Meta:
        db_table = 'statement_items'

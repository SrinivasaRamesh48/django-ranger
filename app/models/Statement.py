from django.db import models
from .time_stamped_model_mixin import TimeStampedModelMixin
class Statement(TimeStampedModelMixin, models.Model):
    statement_id = models.AutoField(primary_key=True)
    due_date = models.DateField()
    archived = models.IntegerField(default=0)
    initial_statement = models.IntegerField(default=0)  
    final_statement = models.IntegerField(default=0)
    amount_past_due = models.DecimalField(max_digits=10, default=0.00, decimal_places=2)
    qbo_invoice_id = models.IntegerField(blank=True, null=True)

    # Relationships
    subscriber = models.ForeignKey('Subscriber', on_delete=models.CASCADE, related_name='statements', db_column='subscriber_id')

    class Meta:
        db_table = "statements"
        ordering = ['-due_date']
    
    def __str__(self):
        return f"Statement {self.statement_id} for Subscriber {self.subscriber_id}"
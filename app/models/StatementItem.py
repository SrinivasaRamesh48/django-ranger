
from django.db import models



class StatementItem(models.Model):
    """Django equivalent of the Laravel StatementItem model."""
    statement_item_id = models.AutoField(primary_key=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    custom = models.TextField(blank=True, null=True)

    # Relationships
    statement = models.ForeignKey('Statement', on_delete=models.CASCADE, related_name='items', db_column='statement_id')
    description = models.ForeignKey("StatementItemDescription", on_delete=models.PROTECT, db_column='statement_item_description_id')
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, null=True, blank=True, db_column='payment_id')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'statement_items'

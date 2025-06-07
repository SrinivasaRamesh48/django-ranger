from django.db import models
# Import related models
from .Statement import Statement # Assuming Statement model exists
from .StatementItemDescription import StatementItemDescription # Assuming StatementItemDescription model exists
from .Payment import Payment     # Assuming Payment model exists

class StatementItem(models.Model):
    statement_item_id = models.AutoField(primary_key=True)
    statement = models.ForeignKey(
        Statement,
        on_delete=models.CASCADE, # If statement is deleted, its items are too
        db_column='statement_id',
        related_name='items'
    )
    statement_item_description = models.ForeignKey(
        StatementItemDescription,
        on_delete=models.SET_NULL, # Assuming item might remain if description is deleted
        null=True, blank=True,
        db_column='statement_item_description_id',
        related_name='statement_items'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2) # Use DecimalField for currency
    payment = models.ForeignKey(
        Payment,
        on_delete=models.SET_NULL, # Assuming item might remain if payment is deleted
        null=True, blank=True,
        db_column='payment_id',
        related_name='statement_items'
    )
    custom = models.BooleanField(default=False) # Assuming 'custom' is a boolean flag
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'statement_items'
        app_label = 'app'

    def __str__(self):
        return f"Statement Item {self.statement_item_id} - Amount: {self.amount}"
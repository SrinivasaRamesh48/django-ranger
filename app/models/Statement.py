from django.db import models

class Statement(models.Model):
    statement_id = models.AutoField(primary_key=True)
    subscriber = models.ForeignKey(
        'Subscriber',
        on_delete=models.CASCADE,
        db_column='subscriber_id',
        related_name='statements'
    )
    due_date = models.DateField()
    archived = models.BooleanField(default=False)
    initial_statement = models.TextField(blank=True, null=True)
    final_statement = models.TextField(blank=True, null=True)
    amount_past_due = models.DecimalField(max_digits=10, decimal_places=2)
    qbo_invoice_id = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'statements'
        app_label = 'app'

    def __str__(self):
        return f"Statement {self.statement_id} - Due: {self.due_date}"
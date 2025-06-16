from django.db import models

class StatementItemType(models.Model):
    """Django equivalent of the Laravel StatementItemType model."""
    statement_item_type_id = models.AutoField(primary_key=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'statement_item_types'

    def __str__(self):
        return self.description[:50]
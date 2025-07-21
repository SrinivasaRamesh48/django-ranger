from rest_framework import serializers
from app.models import StatementItemType


class StatementItemTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatementItemType
        fields = [
            'statement_item_type_id', 'description', 'created_at', 'updated_at'
        ]

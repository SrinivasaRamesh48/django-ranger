from rest_framework import serializers
from app.models import StatementItemDescription, StatementItemType
from app.serializers.statement_item_type_serializer import StatementItemTypeSerializer


class StatementItemDescriptionSerializer(serializers.ModelSerializer):
    type = StatementItemTypeSerializer(read_only=True)
    statement_item_type_id = serializers.PrimaryKeyRelatedField(queryset=StatementItemType.objects.all(), source='type', write_only=True)

    class Meta:
        model = StatementItemDescription
        fields = [
            'statement_item_description_id', 'description', 'created_at', 'updated_at',
            'type', 'statement_item_type_id'
        ]

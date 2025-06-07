from rest_framework import serializers
from app.models import Statement
from app.models.StatementItem import StatementItem
from app.models.StatementItemDescription import StatementItemDescription
from app.models.StatementItemType import StatementItemType

class StatementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statement
        fields = '__all__'

class StatementItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatementItem
        fields = '__all__'

class StatementItemDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatementItemDescription
        fields = '__all__'

class StatementItemTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatementItemType
        fields = '__all__'
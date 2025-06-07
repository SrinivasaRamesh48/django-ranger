from rest_framework import serializers
from app.models.QBOToken import QBOToken

class QBOTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = QBOToken
        fields = '__all__'

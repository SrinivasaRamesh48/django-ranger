from rest_framework import serializers
from app.models import QBOToken


class QBOTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = QBOToken
        fields = ['qbo_token_id', 'access_token', 'refresh_token', 'expires_at', 'created_at', 'updated_at']

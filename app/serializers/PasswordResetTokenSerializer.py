# app/serializers.py

from rest_framework import serializers
from app.models.PasswordResetToken import PasswordResetToken

# ... (your other serializers) ...

class PasswordResetTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = PasswordResetToken
        fields = '__all__'  # Or specify the fields you want to expose
        # fields = ['password_reset_token_id', 'subscriber', 'token', 'expires', 'created_at', 'updated_at']
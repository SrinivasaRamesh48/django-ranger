from rest_framework import serializers
from app.models import InterestFormLog, UsState, User
from app.serializers.us_state_serializer import UsStateSerializer
from app.serializers.user_serializer import UserSerializer


class InterestFormLogSerializer(serializers.ModelSerializer):
    state = UsStateSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)
    state_id = serializers.PrimaryKeyRelatedField(queryset=UsState.objects.all(), source='state', write_only=True)
    updated_by_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='updated_by', write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = InterestFormLog
        fields = [
            'interest_form_log_id', 'name', 'address', 'city', 'zip_code', 'email', 'phone',
            'message', 'notes', 'ip_address', 'created_at', 'updated_at',
            'state', 'updated_by',
            'state_id', 'updated_by_id'
        ]

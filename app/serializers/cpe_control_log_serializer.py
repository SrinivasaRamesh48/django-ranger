from rest_framework import serializers
from app.models import CPEControlLog, CPEControlLogType, User
from app.serializers.cpe_control_log_type_serializer import CPEControlLogTypeSerializer
from app.serializers.user_serializer import UserSerializer


class CPEControlLogSerializer(serializers.ModelSerializer):
    log_type = CPEControlLogTypeSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    canceled_by = UserSerializer(read_only=True)
    cpe_control_log_type_id = serializers.PrimaryKeyRelatedField(queryset=CPEControlLogType.objects.all(), source='log_type', write_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='user', write_only=True)
    canceled_by_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='canceled_by', write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = CPEControlLog
        fields = [
            'cpe_control_log_id', 'created_at', 'updated_at',
            'log_type', 'user', 'canceled_by',
            'cpe_control_log_type_id', 'user_id', 'canceled_by_id'
        ]

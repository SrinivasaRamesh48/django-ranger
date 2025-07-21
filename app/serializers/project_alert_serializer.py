from rest_framework import serializers
from app.models import ProjectAlert, AlertType, Project, User
from app.serializers.alert_type_serializer import AlertTypeSerializer
from app.serializers.project_serializer import ProjectSerializer
from app.serializers.user_serializer import UserSerializer


class ProjectAlertSerializer(serializers.ModelSerializer):
    alert_type = AlertTypeSerializer(read_only=True)
    project = ProjectSerializer(read_only=True)
    activated_by = UserSerializer(read_only=True)
    deactivated_by = UserSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)

    alert_type_id = serializers.PrimaryKeyRelatedField(queryset=AlertType.objects.all(), source='alert_type', write_only=True)
    project_id = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all(), source='project', write_only=True)
    activated_by_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='activated_by', write_only=True, required=False, allow_null=True)
    deactivated_by_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='deactivated_by', write_only=True, required=False, allow_null=True)
    updated_by_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='updated_by', write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = ProjectAlert
        fields = '__all__'

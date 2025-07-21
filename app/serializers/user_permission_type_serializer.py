from rest_framework import serializers
from app.models import UserPermissionType


class UserPermissionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPermissionType
        fields = [
            'user_permission_type_id', 'identifier', 'description',
            'user_permission_category', 'user_permission_subcategory'
        ]

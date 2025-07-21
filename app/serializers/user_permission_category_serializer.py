from rest_framework import serializers
from app.models import UserPermissionCategory


class UserPermissionCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPermissionCategory
        fields = ['user_permission_category_id', 'description']

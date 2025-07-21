from rest_framework import serializers
from app.models import UserPermissionSubcategory
from app.serializers.user_permission_category_serializer import UserPermissionCategorySerializer


class UserPermissionSubcategorySerializer(serializers.ModelSerializer):
    category = UserPermissionCategorySerializer(read_only=True)

    class Meta:
        model = UserPermissionSubcategory
        fields = '__all__'

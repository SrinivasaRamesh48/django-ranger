from rest_framework import serializers
from app.models import UserRoles


class UserRolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRoles
        fields = ['user_role_id', 'description','dispatch']

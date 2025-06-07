# app/serializers.py

from rest_framework import serializers
from app.models.User import User # 
from app.models.UserCompany import UserCompany
from app.models.UserPermissionCategory import UserPermissionCategory
from app.models.UserPermissionDefaults import UserPermissionDefaults
from app. models.UserPermissions import UserPermissions
from app.models.UserPermissionSubcategory import UserPermissionSubcategory
from app. models.UserPermissionType import UserPermissionType
from app.models.UserRoles import UserRoles
from app.models.UserProjects import UserProjects




class UserSerializer(serializers.ModelSerializer):
    # Direct ForeignKey relationships (nested for full representation)
    user_company = serializers.PrimaryKeyRelatedField(queryset=UserCompany.objects.all(), allow_null=True, required=False) # Or UserCompanySerializer(read_only=True)
    user_role = serializers.PrimaryKeyRelatedField(queryset=UserRoles.objects.all(), allow_null=True, required=False) # Or UserRolesSerializer(read_only=True)

    # HasMany relationships (using SerializerMethodField or direct nesting)
    # permissions = UserPermissionsSerializer(many=True, read_only=True) # Nested, if you want all permissions
    # projects = UserProjectsSerializer(many=True, read_only=True) # Nested, if you want all projects

    class Meta:
        model = User
        fields = '__all__' # Or explicitly list them for control
        # IMPORTANT: Make password write_only. It should never be read back.
        extra_kwargs = {
            'password': {'write_only': True}
        }
        # If 'name' is used instead of first_name/last_name, exclude them:
        # exclude = ('first_name', 'last_name') # Only if you define 'name' and set these to None

    # Handle password hashing when creating/updating a user
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User.objects.create(**validated_data)
        if password is not None:
            user.set_password(password) # Use the model's set_password method
            user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password is not None:
            instance.set_password(password) # Hash the new password
        instance.save()
        return instance
    
class UserCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCompany
        fields = '__all__' 

class UserPermissionCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPermissionCategory
        fields = '__all__'

class UserPermissionDefaultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPermissionDefaults
        fields = '__all__'

class UserPermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPermissions
        fields = '__all__'

class UserPermissionSubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPermissionSubcategory
        fields = '__all__'

class UserPermissionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPermissionType
        fields = '__all__'

class UserProjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProjects
        fields = '__all__'
        
        
class UserRolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRoles
        fields = '__all__'
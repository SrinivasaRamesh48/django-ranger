from rest_framework import serializers
from app.models import UserProjects
from app.serializers.user_serializer import UserSerializer
from app.serializers.project_serializer import ProjectSerializer


class UserProjectsSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    project = ProjectSerializer(read_only=True)
    
    class Meta:
        model = UserProjects
        fields = '__all__'

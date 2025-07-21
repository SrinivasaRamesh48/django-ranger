from rest_framework import serializers
from app.models import UserCompany


class UserCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCompany
        fields = ['user_company_id', 'name']

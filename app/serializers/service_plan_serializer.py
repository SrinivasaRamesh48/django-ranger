from rest_framework import serializers
from app.models import ServicePlan


class ServicePlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicePlan
        fields = ['service_plan_id', 'name']

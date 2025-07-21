from rest_framework import serializers
from app.models import SubscriptionType


class SimpleSubscriptionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionType
        fields = ['subscription_type_id', 'name']

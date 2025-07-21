from rest_framework import serializers
from app.models import LeasingStaffRed


class LeasingStaffRedSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeasingStaffRed
        fields = ['leasing_staff_red_id']

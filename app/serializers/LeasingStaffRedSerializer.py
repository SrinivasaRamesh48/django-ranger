# app/serializers.py

from rest_framework import serializers
from app.models.LeasingStaffRed import LeasingStaffRed # Import the model

# ... (your other serializers) ...

class LeasingStaffRedSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeasingStaffRed
        fields = '__all__' # This will include all fields from the model
        # Or explicitly list them:
        # fields = ['leasing_staff_red_id', 'name']
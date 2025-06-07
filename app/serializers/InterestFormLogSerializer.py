# app/serializers.py

from rest_framework import serializers
from app.models.InterestFormLog import InterestFormLog # Import the model
# from .serializers import UsStateSerializer, UserSerializer # Uncomment and define these if you want 
class InterestFormLogSerializer(serializers.ModelSerializer):
    # Optional: If you want nested representations of UsState and User
    # us_state = UsStateSerializer(read_only=True)
    # updated_by = UserSerializer(read_only=True)

    class Meta:
        model = InterestFormLog
        fields = '__all__'
        # Or specify explicit fields if you don't want to expose all:
        # fields = [
        #     'interest_form_log_id', 'name', 'address', 'city', 'state', 'zip_code',
        #     'email', 'phone', 'message', 'notes', 'updated_by', 'ip_address',
        #     'created_at', 'updated_at'
        # ]
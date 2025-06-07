# app/serializers.py

from rest_framework import serializers
from app.models.MultiHomeSubscriberHome import MultiHomeSubscriberHome # Import the model
# from .serializers import HomeSerializer, SubscriberSerializer # Uncomment and define if you want nested output

# ... (your other serializers) ...

class MultiHomeSubscriberHomeSerializer(serializers.ModelSerializer):
    # Optional: If you want nested representations of Home and Subscriber
    # home = HomeSerializer(read_only=True)
    # subscriber = SubscriberSerializer(read_only=True)

    class Meta:
        model = MultiHomeSubscriberHome
        fields = '__all__'
        # Or specify explicit fields if you don't want to expose all:
        # fields = [
        #     'multi_home_subscriber_home_id', 'home', 'subscriber',
        #     'created_at', 'updated_at'
        # ]
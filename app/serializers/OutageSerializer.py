# app/serializers.py

from rest_framework import serializers
from app.models.Outage import Outage 
from app.models.OutageHomesEffected import OutageHomesEffected

# Optional: If you want nested representations of related objects:
# from .serializers import ProjectSerializer, AlertSerializer, OutageHomesEffectedSerializer

# ... (your other serializers) ...

class OutageSerializer(serializers.ModelSerializer):
    # Optional: For nested representations
    # project = ProjectSerializer(read_only=True)
    # alert = AlertSerializer(read_only=True) # If Alert is OneToOneField to Outage, or you want the first alert
    # effected = OutageHomesEffectedSerializer(many=True, read_only=True) # For hasMany relationship

    class Meta:
        model = Outage
        fields = '__all__'
        # Or specify explicit fields:
        # fields = [
        #     'outage_id', 'project', 'resolved', 'email_notices_sent',
        #     'phone_notices_sent', 'phone_message_updated', 'confirmed',
        #     'confirmed_at', 'created_at', 'updated_at'
        # ]

class OutageHomesEffectedSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutageHomesEffected
        fields = '__all__'
        # Or specify explicit fields if you don't want to expose all:
        # fields = [
        #     'id', 'outage', 'home_id', 'created_at', 'updated_at'
        # ]        
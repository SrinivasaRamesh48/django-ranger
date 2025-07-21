from rest_framework import serializers
from app.models import DispatchAppointmentType


class DispatchAppointmentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DispatchAppointmentType
        fields = ['dispatch_appointment_type_id', 'name']

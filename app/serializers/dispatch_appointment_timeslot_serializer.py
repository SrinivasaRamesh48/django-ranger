from rest_framework import serializers
from app.models import DispatchAppointmentTimeslot


class DispatchAppointmentTimeslotSerializer(serializers.ModelSerializer):
    class Meta:
        model = DispatchAppointmentTimeslot
        fields = ['dispatch_appointment_timeslot_id', 'slot_description']

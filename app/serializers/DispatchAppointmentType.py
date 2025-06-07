
from rest_framework import serializers
from app.models.DispatchAppointment import DispatchAppointment
from app.models.DispatchAppointmentType import DispatchAppointmentType
from app.models.DispatchAppointmentTimeslot import DispatchAppointmentTimeslot

class DispatchAppointmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = DispatchAppointment
        fields = '__all__'


class DispatchAppointmentTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = DispatchAppointmentType
        fields = '__all__'


class DispatchAppointmentTimeslotSerializer(serializers.ModelSerializer):

    class Meta:
        model = DispatchAppointmentTimeslot
        fields = '__all__'
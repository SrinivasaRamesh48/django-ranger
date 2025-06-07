# app/serializers.py

from rest_framework import serializers
from app.models.Subscriber import Subscriber
from app.models.SubscriberAlert import SubscriberAlert
from app.models.SubscriberEmailLog import SubscriberEmailLog 
from app.models.SubscriberPaymentMethod import SubscriberPaymentMethod
from app.models.SubscriberSMSLog import SubscriberSMSLog
from app.models.SubscriptionType import SubscriptionType 
# Import related serializers for nesting (if needed)
# from .serializers import HomeSerializer
# from .serializers import ServicePlanSerializer
# from .serializers import NodeSerializer
# from .serializers import TicketSerializer # For open_tickets_info and tickets
# from .serializers import UploadsSerializer
# from .serializers import StatementSerializer # For current_statement and statements
# from .serializers import PaymentSerializer
# from .serializers import SubscriberPaymentMethodSerializer
# from .serializers import MultiHomeSubscriberHomeSerializer
# from .serializers import SubscriberAlertSerializer # For active_alerts

class SubscriberSerializer(serializers.ModelSerializer):
    # For basic FKs, you can use nested serializers or PrimaryKeyRelatedField
    home = HomeSerializer(read_only=True) # Example of nesting
    service_plan = ServicePlanSerializer(read_only=True)
    node = NodeSerializer(read_only=True)

    # Custom properties / filtered relationships
    open_tickets = serializers.SerializerMethodField()
    current_statement = serializers.SerializerMethodField()
    active_alerts = serializers.SerializerMethodField()
    # For full lists, you can directly nest or use SerializerMethodField if you need to filter/order
    tickets = serializers.SerializerMethodField() # To fetch all tickets
    statements = StatementSerializer(many=True, read_only=True) # All statements
    payments = PaymentSerializer(many=True, read_only=True)
    payment_methods = SubscriberPaymentMethodSerializer(many=True, read_only=True)
    multi_homes = MultiHomeSubscriberHomeSerializer(many=True, read_only=True)
    uploads = UploadsSerializer(many=True, read_only=True)

    class Meta:
        model = Subscriber
        fields = '__all__'
        # IMPORTANT: Make password write_only and possibly exclude it from read
        extra_kwargs = {
            'password': {'write_only': True}
        }
        # If you want to explicitly list fields, ensure all fields are covered

    # --- SerializerMethodField implementations ---
    def get_open_tickets(self, obj):
        # Calls the model's property and serializes it
        from .serializers import TicketSerializer # Import locally to avoid circular deps
        qs = obj.open_tickets_info # Access the @property from the model
        return TicketSerializer(qs, many=True, read_only=True).data

    def get_current_statement(self, obj):
        # Calls the model's property and serializes it
        statement_obj = obj.current_statement
        if statement_obj:
            from .serializers import StatementSerializer # Import locally
            return StatementSerializer(statement_obj, read_only=True).data
        return None

    def get_active_alerts(self, obj):
        # Calls the model's property and serializes it
        from .serializers import SubscriberAlertSerializer # Import locally
        qs = obj.active_alerts
        return SubscriberAlertSerializer(qs, many=True, read_only=True).data

    def get_tickets(self, obj):
        # Returns all tickets for the subscriber
        from .serializers import TicketSerializer # Import locally
        return TicketSerializer(obj.tickets.all(), many=True, read_only=True).data

    # --- Password Handling in Serializer (Crucial) ---
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        subscriber = Subscriber.objects.create(**validated_data)
        if password is not None:
            subscriber.set_password(password) # Hash the password
            subscriber.save()
        return subscriber

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        # Update other fields first
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password is not None:
            instance.set_password(password) # Hash the new password

        instance.save()
        return instance
    
class SubscriberAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriberAlert
        fields = '__all__'

class SubscriberEmailLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriberEmailLog
        fields = '__all__'


class SubscriberPaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriberPaymentMethod
        fields = '__all__'


class SubscriberSMSLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriberSMSLog
        fields = '__all__'


class SubscriptionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionType
        fields = '__all__'
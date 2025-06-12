
from rest_framework import serializers
from app.models.Subscriber import Subscriber
from app.models.SubscriberAlert import SubscriberAlert
from app.models.SubscriberEmailLog import SubscriberEmailLog 
from app.models.SubscriberPaymentMethod import SubscriberPaymentMethod
from app.models.SubscriberSMSLog import SubscriberSMSLog
from app.models.SubscriptionType import SubscriptionType 
from app.serializers import HomeSerializer
from app.serializers import ServicePlanSerializer
from app.serializers import NodeSerializer
from app.serializers.TicketSerializer import TicketSerializer 
from app.serializers import UploadsSerializer
from app.serializers import StatementSerializer # For current_statement and statements
from app.serializers import PaymentSerializer
from app.serializers import MultiHomeSubscriberHomeSerializer


class SubscriberSerializer(serializers.ModelSerializer):
    home = HomeSerializer(read_only=True)
    service_plan = ServicePlanSerializer(read_only=True)
    tickets = TicketSerializer(many=True, read_only=True)
    open_tickets = serializers.SerializerMethodField()
    uploads = UploadsSerializer(many=True, read_only=True)
    statement_active = serializers.SerializerMethodField()
    statements = StatementSerializer(many=True, read_only=True)
    payments = PaymentSerializer(many=True, read_only=True)
    # payment_methods = SubscriberPaymentMethodSerializer(many=True, read_only=True)
    multi_homes = MultiHomeSubscriberHomeSerializer(many=True, read_only=True)
    # alerts = SubscriberAlertSerializer(many=True, read_only=True)
    active_alerts = serializers.SerializerMethodField()


    class Meta:
        model = Subscriber
        fields = [
            'subscriber_id', 'home', 'first_name', 'last_name', 'primary_email',
            'username', 'primary_phone', 'service_plan', 'node_id',
            'node_port_number', 'service_activated_on', 'service_deactivated_on',
            'suspended', 'merchant_customer_id', 'autopay_merchant_id',
            'acp_application_id', 'qbo_customer_id', 'multi_home_subscriber',
            'pause_billing', 'created_at', 'updated_at',
            'tickets', 'open_tickets', 'uploads', 'statement_active', 'statements',
            'payments', 'payment_methods', 'multi_homes', 'alerts', 'active_alerts'
        ]
        # 'password' is omitted for security; handle separately if needed for creation/update

    def get_open_tickets(self, obj):
        # Access the custom method defined on the model
        open_tickets = obj.open_tickets()
        return TicketSerializer(open_tickets, many=True).data

    def get_statement_active(self, obj):
        # Access the custom method defined on the model
        statement = obj.statement_active()
        return StatementSerializer(statement).data if statement else None

    def get_active_alerts(self, obj):
        # Access the custom method defined on the model
        active_alerts = obj.active_alerts()
        return SubscriberAlertSerializer(active_alerts, many=True).data
    
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
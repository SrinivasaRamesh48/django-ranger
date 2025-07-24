from rest_framework import serializers
from app.models import Subscriber
from app.models import Home, ServicePlan, Node
from app.serializers.home_serializer import HomeSerializer

from app.serializers.service_plan_serializer import ServicePlanSerializer
from app.serializers.node_serializer import NodeSerializer
from app.serializers.ticket_serializer import TicketSerializer
from app.serializers.statement_serializer import StatementSerializer
from app.serializers.subscriber_payment_method_serializer import SubscriberPaymentMethodSerializer
from app.serializers.multi_home_subscriber_home_serializer import MultiHomeSubscriberHomeSerializer
from app.serializers.subscriber_alert_serializer import SubscriberAlertSerializer   

class SubscriberSerializer(serializers.ModelSerializer):
    home = HomeSerializer(read_only=True)
    service_plan = ServicePlanSerializer(read_only=True)
    node = NodeSerializer(read_only=True)
    tickets = TicketSerializer(many=True, read_only=True)
    open_tickets = serializers.SerializerMethodField()
    statement = serializers.SerializerMethodField()
    statements = StatementSerializer(many=True, read_only=True)
    payment_methods = SubscriberPaymentMethodSerializer(many=True, read_only=True)
    multi_homes = MultiHomeSubscriberHomeSerializer(many=True, read_only=True, source='multihomesubscriberhome_set')
    alerts = serializers.SerializerMethodField()

    home_id = serializers.PrimaryKeyRelatedField(queryset=Home.objects.all(), source='home', write_only=True)
    service_plan_id = serializers.PrimaryKeyRelatedField(queryset=ServicePlan.objects.all(), source='service_plan', write_only=True)
    node_id = serializers.PrimaryKeyRelatedField(queryset=Node.objects.all(), source='node', write_only=True, required=False, allow_null=True)
    payments = serializers.SerializerMethodField()
    
    def get_payments(self, obj):
        from app.serializers.payment_serializer import PaymentSerializer
        return PaymentSerializer(obj.payments.all(), many=True).data

    def get_open_tickets(self, obj):
        """Get open tickets for this subscriber"""
        return TicketSerializer(obj.open_tickets(), many=True).data

    def get_statement(self, obj):
        """Get the active statement for this subscriber"""
        return StatementSerializer(obj.statement()).data if obj.statement() else None
    
    def get_alerts(self, obj):
        active_alerts = obj.alerts.filter(active=True).order_by('-alert_type_id')
        return SubscriberAlertSerializer(active_alerts, many=True).data

    class Meta:
        model = Subscriber
        fields = [
            'subscriber_id', 'first_name', 'last_name', 'primary_email', 'username', 'password',
            'primary_phone', 'service_activated_on', 'service_deactivated_on',
            'suspended', 'merchant_customer_id', 'autopay_merchant_id', 
            'acp_application_id', 'qbo_customer_id', 'multi_home_subscriber', 'pause_billing',
            'created_at', 'updated_at',
            'home', 'home_id',
            'service_plan', 'service_plan_id',
            'node', 'node_id',
            'tickets', 'open_tickets', 'statement', 'statements', 'payments', 'payment_methods',
            'multi_homes', 'alerts', 'payments',
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        } 
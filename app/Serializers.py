from rest_framework import serializers
from app.models import (
    Alert, AlertType, User, Outage, Project, BulkMessageType,
    UsState, CircuitCarrier, Circuit, CPEControlLogType, CPEControlLog,
    DispatchAppointmentType, DispatchAppointmentTimeslot, Ticket,
    MacAddress, NodeClass, NodeType, Subscriber, HomeAlert,
    MeshCPEInstall, Home, NodeFrame, Node, MultiHomeSubscriberHome,
    DowntimeEvent, EmailLogItem, BulkEmailTemplate, BulkPhoneTemplate,
    DispatchAppointment, InterestFormLog, CircuitAlert, OltSnapshot, OntManufacturer, Ont, OutageHomesEffected, PasswordResetToken, Payment, SubscriberPaymentMethod, Statement, PortMacAddress, Builder, SubscriptionType ,ServicePlan, ProjectNetworkType,QBOToken,ProjectAlert,RateLimitLog,ReportType,SavedReport,ServiceChangeSchedule,ServiceChangeScheduleType,LeasingStaffRed,SMSLogItem,StatementItem,StatementItemDescription,StatementItemType,SubscriberAlert,SubscriberEmailLog,SubscriberSMSLog,TicketCategory,TicketEntry,TicketEntryAction,TicketStatus,TicketEntryActionType,TicketStatus,UploadType,Uploads,UserCompany,UserPermissionCategory,UserPermissionDefaults,UserPermissions,UserPermissionSubcategory,UserPermissionType,UserProjects,UserRoles,UsState
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']

class AlertTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertType
        fields = ['alert_type_id', 'name']

class OutageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Outage
        fields = ['outage_id', 'start_time', 'end_time']

class BulkMessageTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BulkMessageType
        fields = ['bulk_message_type_id', 'name']

class UsStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsState
        fields = ['state_id', 'name', 'abbreviation']

class CircuitCarrierSerializer(serializers.ModelSerializer):
    class Meta:
        model = CircuitCarrier
        fields = ['circuit_carrier_id', 'name']

class CircuitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Circuit
        fields = ['circuit_id', 'title']

class CPEControlLogTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CPEControlLogType
        fields = ['cpe_control_log_type_id', 'name']

class DispatchAppointmentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DispatchAppointmentType
        fields = ['dispatch_appointment_type_id', 'name']

class DispatchAppointmentTimeslotSerializer(serializers.ModelSerializer):
    class Meta:
        model = DispatchAppointmentTimeslot
        fields = ['dispatch_appointment_timeslot_id', 'slot_description']

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['ticket_id', 'summary']

class MacAddressSerializer(serializers.ModelSerializer):
    manufacturer = serializers.CharField(read_only=True)
    class Meta:
        model = MacAddress
        fields = ['mac_address_id', 'address', 'manufacturer']

class NodeClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = NodeClass
        fields = ['node_class_id', 'name']

class NodeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NodeType
        fields = ['node_type_id', 'name']

class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = ['subscriber_id', 'service_plan_id', 'service_activated_on']

class HomeAlertSerializer(serializers.ModelSerializer):
    alert_type = AlertTypeSerializer(read_only=True)
    class Meta:
        model = HomeAlert
        fields = ['home_alert_id', 'message', 'active', 'alert_type']

class MeshInstallSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeshCPEInstall
        fields = ['mesh_cpe_install_id', 'address', 'cpe_id']

class HomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Home
        fields = ['home_id', 'address', 'city']

class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = ['node_id', 'hostname']

class NodeFrameSerializer(serializers.ModelSerializer):
    class Meta:
        model = NodeFrame
        fields = ['node_frame_id', 'description']
        
class OntManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = OntManufacturer
        fields = ['ont_manufacturer_id']     

class BuilderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Builder
        fields = ['builder_id', 'name']           

class SubscriptionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionType
        fields = ['subscription_type_id', 'name']


class ServicePlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicePlan
        fields = ['service_plan_id', 'name']

class ProjectNetworkTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectNetworkType
        fields = ["__all__"]

class QBOTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = QBOToken
        fields = ['qbo_token_id', 'access_token', 'refresh_token', 'expires_at', 'created_at', 'updated_at']    

class ServiceChangeScheduleTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceChangeScheduleType
        fields = ['__all__']


class LeasingStaffRedSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeasingStaffRed
        fields = ['leasing_staff_red_id']

class TicketEntryActionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketEntryActionType
        fields = ['ticket_entry_action_type_id', 'name']

class TicketStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketStatus
        fields = ['ticket_status_id', 'name']
class UploadTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadType
        fields = ['upload_type_id', 'description']

class UserCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCompany
        fields = ['user_company_id', 'name']


class UserPermissionCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPermissionCategory
        fields = ['user_permission_category_id', 'description'] 

class UserRolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRoles
        fields = ['user_role_id', 'name'] 


class UsStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsState
        fields = ['us_state_id', 'name',]

# --- Main Serializers ---
class ProjectSerializer(serializers.ModelSerializer):
    us_state = UsStateSerializer(read_only=True)
    builder = BuilderSerializer(read_only=True)
    subscription_type = SubscriptionTypeSerializer(read_only=True)
    service_plan = ServicePlanSerializer(read_only=True)
    circuit = CircuitSerializer(read_only=True)

    state_id = serializers.PrimaryKeyRelatedField(queryset=UsState.objects.all(), source='us_state', write_only=True)
    builder_id = serializers.PrimaryKeyRelatedField(queryset=Builder.objects.all(), source='builder', write_only=True, required=False, allow_null=True)
    subscription_type_id = serializers.PrimaryKeyRelatedField(queryset=SubscriptionType.objects.all(), source='subscription_type', write_only=True)
    bulk_service_plan_id = serializers.PrimaryKeyRelatedField(queryset=ServicePlan.objects.all(), source='service_plan', write_only=True, required=False, allow_null=True)
    circuit_id = serializers.PrimaryKeyRelatedField(queryset=Circuit.objects.all(), source='circuit', write_only=True, required=False, allow_null=True)

    class Meta:
        model = Project
        fields = [
            'project_id', 'name', 'address', 'city', 'zip_code', 'longitude', 'latitude', 
            'activation_date', 'active', 'domain_name', 'free_month', 'qbo_customer_id', 
            'rm_property_id', 'created_at', 'updated_at',
            'us_state', 'state_id',
            'builder', 'builder_id',
            'subscription_type', 'subscription_type_id',
            'service_plan', 'bulk_service_plan_id',
            'circuit', 'circuit_id'
        ]

class AlertSerializer(serializers.ModelSerializer):
    alert_type = AlertTypeSerializer(read_only=True)
    activated_by = UserSerializer(read_only=True)
    deactivated_by = UserSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)
    alert_type_id = serializers.PrimaryKeyRelatedField(queryset=AlertType.objects.all(), source='alert_type', write_only=True)
    activated_by_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='activated_by', write_only=True, required=False, allow_null=True)
    deactivated_by_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='deactivated_by', write_only=True, required=False, allow_null=True)
    updated_by_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='updated_by', write_only=True, required=False, allow_null=True)
    outage_id = serializers.PrimaryKeyRelatedField(queryset=Outage.objects.all(), source='outage', write_only=True, required=False, allow_null=True)
    class Meta:
        model = Alert
        fields = [
            'alert_id', 'message', 'active', 'alert_type', 'alert_type_id',
            'activated_by', 'activated_by_id', 'deactivated_by', 'deactivated_by_id',
            'updated_by', 'updated_by_id', 'outage_id', 'created_at', 'updated_at'
        ]

class BulkEmailTemplateSerializer(serializers.ModelSerializer):
    message_type = BulkMessageTypeSerializer(read_only=True)
    bulk_message_type_id = serializers.PrimaryKeyRelatedField(queryset=BulkMessageType.objects.all(), source='message_type', write_only=True)
    class Meta:
        model = BulkEmailTemplate
        fields = [
            'bulk_email_template_id', 'description', 'subject', 'body',
            'message_type', 'bulk_message_type_id', 'created_at', 'updated_at'
        ]

class BulkPhoneTemplateSerializer(serializers.ModelSerializer):
    message_type = BulkMessageTypeSerializer(read_only=True)
    bulk_message_type_id = serializers.PrimaryKeyRelatedField(queryset=BulkMessageType.objects.all(), source='message_type', write_only=True)
    class Meta:
        model = BulkPhoneTemplate
        fields = [
            'bulk_phone_template_id', 'description', 'body',
            'message_type', 'bulk_message_type_id', 'created_at', 'updated_at'
        ]

class CircuitSerializer(serializers.ModelSerializer):
    circuit_carrier = CircuitCarrierSerializer(read_only=True)
    state = UsStateSerializer(read_only=True)
    circuit_carrier_id = serializers.PrimaryKeyRelatedField(queryset=CircuitCarrier.objects.all(), source='circuit_carrier', write_only=True)
    state_id = serializers.PrimaryKeyRelatedField(queryset=UsState.objects.all(), source='state', write_only=True, required=False, allow_null=True)
    class Meta:
        model = Circuit
        fields = [
            'circuit_id', 'title', 'address', 'city', 'zip_code', 'circuit_id_a',
            'circuit_id_z', 'contact_number', 'activation_date', 'mbps_speed',
            'facility_assignment', 'media_type', 'created_at', 'updated_at',
            'circuit_carrier', 'state',
            'circuit_carrier_id', 'state_id'
        ]

class CircuitAlertSerializer(serializers.ModelSerializer):
    alert_type = AlertTypeSerializer(read_only=True)
    circuit = CircuitSerializer(read_only=True)
    activated_by = UserSerializer(read_only=True)
    deactivated_by = UserSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)
    alert_type_id = serializers.PrimaryKeyRelatedField(queryset=AlertType.objects.all(), source='alert_type', write_only=True)
    circuit_id = serializers.PrimaryKeyRelatedField(queryset=Circuit.objects.all(), source='circuit', write_only=True)
    activated_by_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='activated_by', write_only=True, required=False, allow_null=True)
    deactivated_by_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='deactivated_by', write_only=True, required=False, allow_null=True)
    updated_by_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='updated_by', write_only=True, required=False, allow_null=True)
    class Meta:
        model = CircuitAlert
        fields = [
            'circuit_alert_id', 'message', 'active', 'created_at', 'updated_at',
            'alert_type', 'circuit', 'activated_by', 'deactivated_by', 'updated_by',
            'alert_type_id', 'circuit_id', 'activated_by_id', 'deactivated_by_id', 'updated_by_id'
        ]

class CPEControlLogSerializer(serializers.ModelSerializer):
    log_type = CPEControlLogTypeSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    canceled_by = UserSerializer(read_only=True)
    cpe_control_log_type_id = serializers.PrimaryKeyRelatedField(queryset=CPEControlLogType.objects.all(), source='log_type', write_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='user', write_only=True)
    canceled_by_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='canceled_by', write_only=True, required=False, allow_null=True)
    class Meta:
        model = CPEControlLog
        fields = [
            'cpe_control_log_id', 'created_at', 'updated_at',
            'log_type', 'user', 'canceled_by',
            'cpe_control_log_type_id', 'user_id', 'canceled_by_id'
        ]

class DispatchAppointmentSerializer(serializers.ModelSerializer):
    appointment_type = DispatchAppointmentTypeSerializer(read_only=True)
    technician = UserSerializer(read_only=True)
    timeslot = DispatchAppointmentTimeslotSerializer(read_only=True)
    ticket = TicketSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)
    canceled_by = UserSerializer(read_only=True)
    dispatch_appointment_type_id = serializers.PrimaryKeyRelatedField(queryset=DispatchAppointmentType.objects.all(), source='appointment_type', write_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='technician', write_only=True)
    dispatch_appointment_timeslot_id = serializers.PrimaryKeyRelatedField(queryset=DispatchAppointmentTimeslot.objects.all(), source='timeslot', write_only=True)
    ticket_id = serializers.PrimaryKeyRelatedField(queryset=Ticket.objects.all(), source='ticket', write_only=True, required=False, allow_null=True)
    created_by_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='created_by', write_only=True)
    canceled_by_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='canceled_by', write_only=True, required=False, allow_null=True)
    class Meta:
        model = DispatchAppointment
        fields = [
            'dispatch_appointment_id', 'date', 'notes', 'completion_notes',
            'completed_on', 'wiring_certified', 'wiring_repaired', 'canceled_on', 'pte', 'pets',
            'created_at', 'updated_at',
            'appointment_type', 'technician', 'timeslot', 'ticket', 'created_by', 'canceled_by',
            'dispatch_appointment_type_id', 'user_id', 'dispatch_appointment_timeslot_id',
            'ticket_id', 'created_by_id', 'canceled_by_id'
        ]

class DowntimeEventSerializer(serializers.ModelSerializer):
    outage = OutageSerializer(read_only=True)
    project = ProjectSerializer(read_only=True)
    outage_id = serializers.PrimaryKeyRelatedField(queryset=Outage.objects.all(), source='outage', write_only=True)
    project_id = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all(), source='project', write_only=True, required=False, allow_null=True)
    class Meta:
        model = DowntimeEvent
        fields = [
            'downtime_event_id', 'created_at', 'updated_at',
            'outage', 'project',
            'outage_id', 'project_id',
        ]

class EmailLogItemSerializer(serializers.ModelSerializer):
    outage = OutageSerializer(read_only=True)
    bulk_message_type = BulkMessageTypeSerializer(read_only=True)
    outage_id = serializers.PrimaryKeyRelatedField(queryset=Outage.objects.all(), source='outage', write_only=True, required=False, allow_null=True)
    bulk_message_type_id = serializers.PrimaryKeyRelatedField(queryset=BulkMessageType.objects.all(), source='bulk_message_type', write_only=True, required=False, allow_null=True)
    class Meta:
        model = EmailLogItem
        fields = [
            'email_log_item_id', 'subject', 'body', 'created_at', 'updated_at',
            'outage', 'bulk_message_type',
            'outage_id', 'bulk_message_type_id'
        ]

class HomeAlertSerializer(serializers.ModelSerializer):
    alert_type = AlertTypeSerializer(read_only=True)
    home = HomeSerializer(read_only=True)
    activated_by = UserSerializer(read_only=True)
    deactivated_by = UserSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)
    alert_type_id = serializers.PrimaryKeyRelatedField(queryset=AlertType.objects.all(), source='alert_type', write_only=True)
    home_id = serializers.PrimaryKeyRelatedField(queryset=Home.objects.all(), source='home', write_only=True)
    activated_by_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='activated_by', write_only=True, required=False, allow_null=True)
    deactivated_by_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='deactivated_by', write_only=True, required=False, allow_null=True)
    updated_by_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='updated_by', write_only=True, required=False, allow_null=True)
    class Meta:
        model = HomeAlert
        fields = [
            'home_alert_id', 'message', 'active', 'created_at', 'updated_at',
            'alert_type', 'home', 'activated_by', 'deactivated_by', 'updated_by',
            'alert_type_id', 'home_id', 'activated_by_id', 'deactivated_by_id', 'updated_by_id'
        ]
        
class MacAddressSerializer(serializers.ModelSerializer):
    home = HomeSerializer(read_only=True)
    manufacturer = serializers.CharField(read_only=True)
    default_credentials = serializers.DictField(read_only=True)
    home_id = serializers.PrimaryKeyRelatedField(queryset=Home.objects.all(), source='home', write_only=True)
    class Meta:
        model = MacAddress
        fields = [
            'mac_address_id', 'address', 'cpe_id', 'cpe_serial_number', 
            'firmware_update', 'firmware_update_manual', 'manual_registration',
            'created_at', 'updated_at',
            'home', 'home_id', 'manufacturer', 'default_credentials'
        ]

class MeshCPEInstallSerializer(serializers.ModelSerializer):
    home = HomeSerializer(read_only=True)
    home_id = serializers.PrimaryKeyRelatedField(queryset=Home.objects.all(), source='home', write_only=True)
    class Meta:
        model = MeshCPEInstall
        fields = [
            'mesh_cpe_install_id', 'address', 'cpe_id', 'cpe_serial_number',
            'created_at', 'updated_at',
            'home', 'home_id'
        ]

class MultiHomeSubscriberHomeSerializer(serializers.ModelSerializer):
    home = HomeSerializer(read_only=True)
    subscriber = SubscriberSerializer(read_only=True)
    home_id = serializers.PrimaryKeyRelatedField(queryset=Home.objects.all(), source='home', write_only=True)
    subscriber_id = serializers.PrimaryKeyRelatedField(queryset=Subscriber.objects.all(), source='subscriber', write_only=True)
    class Meta:
        model = MultiHomeSubscriberHome
        fields = [
            'multi_home_subscriber_home_id', 'created_at', 'updated_at',
            'home', 'subscriber', 'home_id', 'subscriber_id'
        ]

class NodeFrameSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True)
    nodes = NodeSerializer(many=True, read_only=True)
    project_id = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all(), source='project', write_only=True)
    class Meta:
        model = NodeFrame
        fields = [
            'node_frame_id', 'description', 'created_at', 'updated_at',
            'project', 'project_id', 'nodes'
        ]

class NodeSerializer(serializers.ModelSerializer):
    node_frame = NodeFrameSerializer(read_only=True)
    node_class = NodeClassSerializer(read_only=True)
    node_type = NodeTypeSerializer(read_only=True)
    project = ProjectSerializer(read_only=True)
    homes = HomeSerializer(many=True, read_only=True)
    node_frame_id = serializers.PrimaryKeyRelatedField(queryset=NodeFrame.objects.all(), source='node_frame', write_only=True)
    node_class_id = serializers.PrimaryKeyRelatedField(queryset=NodeClass.objects.all(), source='node_class', write_only=True)
    node_type_id = serializers.PrimaryKeyRelatedField(queryset=NodeType.objects.all(), source='node_type', write_only=True)
    project_id = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all(), source='project', write_only=True)
    class Meta:
        model = Node
        fields = [
            'node_id', 'hostname', 'ip_address', 'mac_address', 'serial_number', 'dns_ip_address',
            'created_at', 'updated_at',
            'node_frame', 'node_class', 'node_type', 'project', 'homes',
            'node_frame_id', 'node_class_id', 'node_type_id', 'project_id'
        ]

class HomeSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True)
    state = UsStateSerializer(read_only=True)
    mac_address = MacAddressSerializer(read_only=True)
    node = NodeSerializer(read_only=True)
    wiring_certified_by = UserSerializer(read_only=True)
    subscribers = SubscriberSerializer(many=True, read_only=True)
    alerts = HomeAlertSerializer(many=True, read_only=True)
    mesh_installs = MeshInstallSerializer(many=True, read_only=True)
    active_subscriber = SubscriberSerializer(read_only=True)
    project_id = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all(), source='project', write_only=True)
    state_id = serializers.PrimaryKeyRelatedField(queryset=UsState.objects.all(), source='state', write_only=True)
    node_id = serializers.PrimaryKeyRelatedField(queryset=Node.objects.all(), source='node', write_only=True)
    wiring_certified_by_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='wiring_certified_by', write_only=True, required=False, allow_null=True)
    class Meta:
        model = Home
        fields = [
            'home_id', 'address', 'city', 'zip_code', 'unit', 'ip_address',
            'node_switch_unit', 'node_switch_module', 'node_port_num',
            'wiring_certified_on', 'exclude_from_reports', 'created_at', 'updated_at',
            'project', 'state', 'mac_address', 'node', 'wiring_certified_by',
            'project_id', 'state_id', 'node_id', 'wiring_certified_by_id',
            'subscribers', 'alerts', 'mesh_installs', 'active_subscriber'
        ]

class InterestFormLogSerializer(serializers.ModelSerializer):
    state = UsStateSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)
    state_id = serializers.PrimaryKeyRelatedField(queryset=UsState.objects.all(), source='state', write_only=True)
    updated_by_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='updated_by', write_only=True, required=False, allow_null=True)
    class Meta:
        model = InterestFormLog
        fields = [
            'interest_form_log_id', 'name', 'address', 'city', 'zip_code', 'email', 'phone',
            'message', 'notes', 'ip_address', 'created_at', 'updated_at',
            'state', 'updated_by',
            'state_id', 'updated_by_id'
        ]
        
class OltSnapshotSerializer(serializers.ModelSerializer):
    node = NodeSerializer(read_only=True)
    node_id = serializers.PrimaryKeyRelatedField(queryset=Node.objects.all(), source='node', write_only=True)
    
    class Meta:
        model = OltSnapshot
        fields = [
            'id', 'olt_ip_address', 'interface', 'fsan', 'ont_model', 'ont_active_version', 
            'ont_standby_version', 'ont_rx_power', 'ont_tx_power', 'distance', 'created_at',
            'node', 'node_id'
        ]        


class OntSerializer(serializers.ModelSerializer):
    """Serializes Ont instances for API responses."""
    home = HomeSerializer(read_only=True)
    node = NodeSerializer(read_only=True)
    manufacturer = OntManufacturerSerializer(read_only=True)

    home_id = serializers.PrimaryKeyRelatedField(queryset=Home.objects.all(), source='home', write_only=True)
    node_id = serializers.PrimaryKeyRelatedField(queryset=Node.objects.all(), source='node', write_only=True)
    ont_manufacturer_id = serializers.PrimaryKeyRelatedField(queryset=OntManufacturer.objects.all(), source='manufacturer', write_only=True)

    class Meta:
        model = Ont
        fields = [
            'ont_id', 'fsan', 'mac_address', 'serial_number', 'interface', 'model_id',
            'ont_version', 'software_version', 'ont_rx_power', 'olt_rx_power',
            'distance', 'last_pulled', 'created_at', 'updated_at',
            'home', 'home_id',
            'node', 'node_id',
            'manufacturer', 'ont_manufacturer_id'
        ]        

class OutageSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True)
    effected_homes = HomeSerializer(many=True, read_only=True)
    alert = AlertSerializer(read_only=True)
    project_id = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all(), source='project', write_only=True)
    class Meta:
        model = Outage
        fields = [
            'outage_id', 'resolved', 'email_notices_sent', 'phone_notices_sent',
            'phone_message_updated', 'confirmed', 'confirmed_at',
            'created_at', 'updated_at',
            'project', 'project_id',
            'effected_homes', 'alert'
        ]        
        
        
        
class OutageHomesEffectedSerializer(serializers.ModelSerializer):
    home = HomeSerializer(read_only=True)
    outage = OutageSerializer(read_only=True)
    home_id = serializers.PrimaryKeyRelatedField(queryset=Home.objects.all(), source='home', write_only=True)
    outage_id = serializers.PrimaryKeyRelatedField(queryset=Outage.objects.all(), source='outage', write_only=True)

    class Meta:
        model = OutageHomesEffected
        fields = [
            'outage_homes_effected_id',
            'home', 'home_id',
            'outage', 'outage_id',
            'created_at', 'updated_at'
        ]        
        
class PasswordResetTokenSerializer(serializers.ModelSerializer):
    subscriber = SubscriberSerializer(read_only=True)
    subscriber_id = serializers.PrimaryKeyRelatedField(queryset=Subscriber.objects.all(), source='subscriber', write_only=True)

    class Meta:
        model = PasswordResetToken
        fields = [
            'password_reset_token_id', 'token', 'expires',
            'subscriber', 'subscriber_id',
            'created_at', 'updated_at'
        ]
 
class PaymentSerializer(serializers.ModelSerializer):
    subscriber = SubscriberSerializer(read_only=True)
    # statement = StatementSerializer(read_only=True)
    # payment_method = SubscriberPaymentMethodSerializer(read_only=True)

    subscriber_id = serializers.PrimaryKeyRelatedField(queryset=Subscriber.objects.all(), source='subscriber', write_only=True)
    statement_id = serializers.PrimaryKeyRelatedField(queryset=Statement.objects.all(), source='statement', write_only=True)
    subscriber_payment_method_id = serializers.PrimaryKeyRelatedField(queryset=SubscriberPaymentMethod.objects.all(), source='payment_method', write_only=True)

    class Meta:
        model = Payment
        fields = [
            'payment_id', 'amount', 'merchant_id', 'autopay_merchant_id', 'qbo_payment_id',
            'created_at', 'updated_at',
            'subscriber', 'subscriber_id',
            'statement', 'statement_id',
            'payment_method', 'subscriber_payment_method_id'
        ]

class PortMacAddressSerializer(serializers.ModelSerializer):
    node = NodeSerializer(read_only=True)
    mac_address_found = MacAddressSerializer(read_only=True)
    home_found = HomeSerializer(read_only=True)

    node_Id = serializers.PrimaryKeyRelatedField(queryset=Node.objects.all(), source='node', write_only=True)

    class Meta:
        model = PortMacAddress
        fields = [
            'id', 'node_Id', 'node_switch_unit', 'node_switch_module', 'mac_address',
            'node_port_vlanid', 'node_oper_status', 'node_admin_status', 'node_rate_up',
            'node_rate_down', 'created_at',
            'node', 'mac_address_found', 'home_found'
        ]



class ProjectAlertSerializer(serializers.ModelSerializer):
    alert_type = AlertTypeSerializer(read_only=True)
    project = ProjectSerializer(read_only=True)
    activated_by = UserSerializer(read_only=True)
    deactivated_by = UserSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)

    alert_type_id = serializers.PrimaryKeyRelatedField(queryset=AlertType.objects.all(), source='alert_type', write_only=True)
    project_id = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all(), source='project', write_only=True)
    activated_by_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='activated_by', write_only=True, required=False, allow_null=True)
    deactivated_by_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='deactivated_by', write_only=True, required=False, allow_null=True)
    updated_by_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='updated_by', write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = ProjectAlert
        fields = [
            'project_alert_id', 'message', 'active', 'created_at', 'updated_at',
            'alert_type', 'project', 'activated_by', 'deactivated_by', 'updated_by',
            'alert_type_id', 'project_id', 'activated_by_id', 'deactivated_by_id', 'updated_by_id'
        ]

class RateLimitLogSerializer(serializers.ModelSerializer):
    home = HomeSerializer(read_only=True)
    home_id = serializers.PrimaryKeyRelatedField(queryset=Home.objects.all(), source='home', write_only=True)
    
    class Meta:
        model = RateLimitLog
        fields = [
            'rate_limit_log_id', 'success', 'rate', 'result', 
            'created_at', 'updated_at',
            'home', 'home_id'
        ]
        
        
        
class SavedReportSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    report_type_id = serializers.PrimaryKeyRelatedField(queryset=ReportType.objects.all(), source='type', write_only=True)

    class Meta:
        model = SavedReport
        fields = [
            'saved_report_id', 'title', 'description', 'data', 
            'created_at', 'updated_at', 'type', 'report_type_id'
        ]

    def get_type(self, obj):
        return ReportTypeSerializer(obj.type).data if obj.type else None        


class ReportTypeSerializer(serializers.ModelSerializer):
    saved_reports = SavedReportSerializer(many=True, read_only=True)
    class Meta:
        model = ReportType
        fields = ['report_type_id', 'saved_reports']
        
class ServiceChangeScheduleSerializer(serializers.ModelSerializer):
    subscriber = SubscriberSerializer(read_only=True)
    service_plan = ServicePlanSerializer(read_only=True)
    ticket_entry = TicketSerializer(read_only=True)
    type = ServiceChangeScheduleTypeSerializer(read_only=True)
    leasing_staff_red = LeasingStaffRedSerializer(read_only=True)

    subscriber_id = serializers.PrimaryKeyRelatedField(queryset=Subscriber.objects.all(), source='subscriber', write_only=True)
    service_plan_id = serializers.PrimaryKeyRelatedField(queryset=ServicePlan.objects.all(), source='service_plan', write_only=True)
    ticket_entry_id = serializers.PrimaryKeyRelatedField(queryset=Ticket.objects.all(), source='ticket_entry', write_only=True, required=False, allow_null=True)
    service_change_schedule_type_id = serializers.PrimaryKeyRelatedField(queryset=ServiceChangeScheduleType.objects.all(), source='type', write_only=True)
    leasing_staff_red_id = serializers.PrimaryKeyRelatedField(queryset=LeasingStaffRed.objects.all(), source='leasing_staff_red', write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = ServiceChangeSchedule
        fields = [
            'service_change_schedule_id', 'ssid_1', 'passkey_1', 'ssid_2', 'passkey_2', 
            'process_on', 'processed', 'canceled', 'created_at', 'updated_at',
            'subscriber', 'subscriber_id',
            'service_plan', 'service_plan_id',
            'ticket_entry', 'ticket_entry_id',
            'type', 'service_change_schedule_type_id',
            'leasing_staff_red', 'leasing_staff_red_id'
        ]        

class SMSLogItemSerializer(serializers.ModelSerializer):
    outage = OutageSerializer(read_only=True)
    bulk_message_type = BulkMessageTypeSerializer(read_only=True)
    
    outage_id = serializers.PrimaryKeyRelatedField(queryset=Outage.objects.all(), source='outage', write_only=True, required=False, allow_null=True)
    bulk_message_type_id = serializers.PrimaryKeyRelatedField(queryset=BulkMessageType.objects.all(), source='bulk_message_type', write_only=True, required=False, allow_null=True)

    class Meta:
        model = SMSLogItem
        fields = [
            'sms_log_item_id', 'body', 'created_at', 'updated_at',
            'outage', 'outage_id',
            'bulk_message_type', 'bulk_message_type_id'
        ]
    
class StatementItemTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatementItemType
        fields = [
            'statement_item_type_id', 'description', 'created_at', 'updated_at'
        ]    
       
class StatementItemDescriptionSerializer(serializers.ModelSerializer):
    type = StatementItemTypeSerializer(read_only=True)
    statement_item_type_id = serializers.PrimaryKeyRelatedField(queryset=StatementItemType.objects.all(), source='type', write_only=True)

    class Meta:
        model = StatementItemDescription
        fields = [
            'statement_item_description_id', 'description', 'created_at', 'updated_at',
            'type', 'statement_item_type_id'
        ]


class StatementItemSerializer(serializers.ModelSerializer):
    description = StatementItemDescriptionSerializer(read_only=True)
    payment = PaymentSerializer(read_only=True)

    statement_item_description_id = serializers.PrimaryKeyRelatedField(queryset=StatementItemDescription.objects.all(), source='description', write_only=True)
    payment_id = serializers.PrimaryKeyRelatedField(queryset=Payment.objects.all(), source='payment', write_only=True, required=False, allow_null=True)

    class Meta:
        model = StatementItem
        fields = [
            'statement_item_id', 'amount', 'custom', 'created_at', 'updated_at',
            'description', 'statement_item_description_id',
            'payment', 'payment_id'
        ]
        
        
class StatementSerializer(serializers.ModelSerializer):
    """Serializes Statement instances for API responses."""
    subscriber = SubscriberSerializer(read_only=True)
    items = StatementItemSerializer(many=True, read_only=True)
    
    subscriber_id = serializers.PrimaryKeyRelatedField(queryset=Subscriber.objects.all(), source='subscriber', write_only=True)

    class Meta:
        model = Statement
        fields = [
            'statement_id', 'due_date', 'archived', 'initial_statement', 
            'final_statement', 'amount_past_due', 'qbo_invoice_id',
            'created_at', 'updated_at',
            'subscriber', 'subscriber_id',
            'items'
        ]
        
class SubscriberAlertSerializer(serializers.ModelSerializer):
    alert_type = AlertTypeSerializer(read_only=True)
    subscriber = SubscriberSerializer(read_only=True)
    activated_by = UserSerializer(read_only=True)
    deactivated_by = UserSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)

    alert_type_id = serializers.PrimaryKeyRelatedField(queryset=AlertType.objects.all(), source='alert_type', write_only=True)
    subscriber_id = serializers.PrimaryKeyRelatedField(queryset=Subscriber.objects.all(), source='subscriber', write_only=True)
    activated_by_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='activated_by', write_only=True, required=False, allow_null=True)
    deactivated_by_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='deactivated_by', write_only=True, required=False, allow_null=True)
    updated_by_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='updated_by', write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = SubscriberAlert
        fields = [
            'subscriber_alert_id', 'message', 'active', 'created_at', 'updated_at',
            'alert_type', 'subscriber', 'activated_by', 'deactivated_by', 'updated_by',
            'alert_type_id', 'subscriber_id', 'activated_by_id', 'deactivated_by_id', 'updated_by_id'
        ]  
        
class SubscriberEmailLogSerializer(serializers.ModelSerializer):
    item = EmailLogItemSerializer(read_only=True)
    subscriber = SubscriberSerializer(read_only=True)

    email_log_item_id = serializers.PrimaryKeyRelatedField(queryset=EmailLogItem.objects.all(), source='item', write_only=True)
    subscriber_id = serializers.PrimaryKeyRelatedField(queryset=Subscriber.objects.all(), source='subscriber', write_only=True)

    class Meta:
        model = SubscriberEmailLog
        fields = [
            'subscriber_email_log_id', 'sent_to', 'success', 
            'created_at', 'updated_at',
            'item', 'email_log_item_id',
            'subscriber', 'subscriber_id'
        ]  
        
class SubscriberPaymentMethodSerializer(serializers.ModelSerializer):
    subscriber = SubscriberSerializer(read_only=True)
    subscriber_id = serializers.PrimaryKeyRelatedField(queryset=Subscriber.objects.all(), source='subscriber', write_only=True)

    class Meta:
        model = SubscriberPaymentMethod
        fields = [
            'subscriber_payment_method_id', 'nickname', 'card_exp_datetime', 
            'merchant_payment_method_id', 'created_at', 'updated_at',
            'subscriber', 'subscriber_id'
        ]
                    
        
class SubscriberSerializer(serializers.ModelSerializer):
    home = HomeSerializer(read_only=True)
    service_plan = ServicePlanSerializer(read_only=True)
    node = NodeSerializer(read_only=True)
    tickets = TicketSerializer(many=True, read_only=True)
    open_tickets = TicketSerializer(many=True, read_only=True)
    statement = StatementSerializer(read_only=True)
    statements = StatementSerializer(many=True, read_only=True)
    payments = PaymentSerializer(many=True, read_only=True)
    payment_methods = SubscriberPaymentMethodSerializer(many=True, read_only=True)
    multi_homes = MultiHomeSubscriberHomeSerializer(many=True, read_only=True, source='multihomesubscriberhome_set')
    alerts = SubscriberAlertSerializer(many=True, read_only=True, source='active_alerts')

    home_id = serializers.PrimaryKeyRelatedField(queryset=Home.objects.all(), source='home', write_only=True)
    service_plan_id = serializers.PrimaryKeyRelatedField(queryset=ServicePlan.objects.all(), source='service_plan', write_only=True)
    node_id = serializers.PrimaryKeyRelatedField(queryset=Node.objects.all(), source='node', write_only=True, required=False, allow_null=True)

    class Meta:
        model = Subscriber
        fields = [
            'subscriber_id', 'first_name', 'last_name', 'primary_email', 'username', 'password',
            'primary_phone', 'node_port_number', 'service_activated_on', 'service_deactivated_on',
            'suspended', 'merchant_customer_id', 'autopay_merchant_id', 
            'acp_application_id', 'qbo_customer_id', 'multi_home_subscriber', 'pause_billing',
            'created_at', 'updated_at',
            'home', 'home_id',
            'service_plan', 'service_plan_id',
            'node', 'node_id',
            'tickets', 'open_tickets', 'statement', 'statements', 'payments', 'payment_methods',
            'multi_homes', 'alerts'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }        
        
class SubscriberSMSLogSerializer(serializers.ModelSerializer):
    item = SMSLogItemSerializer(read_only=True)
    subscriber = SubscriberSerializer(read_only=True)

    sms_log_item_id = serializers.PrimaryKeyRelatedField(queryset=SMSLogItem.objects.all(), source='item', write_only=True)
    subscriber_id = serializers.PrimaryKeyRelatedField(queryset=Subscriber.objects.all(), source='subscriber', write_only=True)

    class Meta:
        model = SubscriberSMSLog
        fields = [
            'subscriber_sms_log_id', 'sent_to', 'success', 
            'created_at', 'updated_at',
            'item', 'sms_log_item_id',
            'subscriber', 'subscriber_id'
        ]        
        
class SimpleSubscriptionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionType
        fields = ['subscription_type_id', 'name']
  
class TicketCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketCategory
        fields = ['ticket_category_id', 'description']  
  
class TicketEntryActionSerializer(serializers.ModelSerializer):
    type = TicketEntryActionTypeSerializer(read_only=True)
    ticket_entry_action_type_id = serializers.PrimaryKeyRelatedField(queryset=TicketEntryActionType.objects.all(), source='type', write_only=True)

    class Meta:
        model = TicketEntryAction
        fields = [
            'ticket_entry_action_id',
            'type', 'ticket_entry_action_type_id'
        ]  
  
class TicketEntrySerializer(serializers.ModelSerializer):
    """
    A comprehensive serializer for the TicketEntry model that includes
    details from related models to provide a rich API response.
    """
    # Nest a serializer to show user details instead of just the user ID.
    # user = UserSerializer(read_only=True) # Recommended approach
    user_info = serializers.CharField(source='user.username', read_only=True)

    # Nest a serializer for a one-to-many relationship
    actions = TicketEntryActionSerializer(many=True, read_only=True)

    # Use a SerializerMethodField to fetch and represent related data
    # that isn't a direct relationship on the model.
    latest_dispatch_appointment = serializers.SerializerMethodField()
    
    # Calculate the duration of the entry on the fly
    duration_minutes = serializers.SerializerMethodField()

    class Meta:
        model = TicketEntry
        fields = [
            'id',
            'ticket',
            'user',
            'user_info', # More readable than just 'user' id
            'description',
            'notes_private',
            'start_time',
            'end_time',
            'duration_minutes',
            'submitted',
            'actions',
            'latest_dispatch_appointment',
            'created_at',
            'updated_at',
        ]
        # Make fields like 'user' write-only, as the user is set from the request,
        # not from the request body.
        read_only_fields = ['created_at', 'updated_at']
        extra_kwargs = {
            'user': {'write_only': True}
        }


    def get_latest_dispatch_appointment(self, obj):
        """
        Gets the most recent dispatch appointment associated with the entry's ticket.
        This mirrors the `dispatch_appointment` relationship in Laravel.
        """
        appointment = obj.ticket.dispatch_appointments.order_by('-id').first()
        if appointment:
            # You could use another serializer here for more detail
            return {'id': appointment.id, 'appointment_date': appointment.appointment_date}
        return None
        
    def get_duration_minutes(self, obj):
        """
        Calculates the difference between end_time and start_time in minutes.
        """
        if obj.end_time and obj.start_time:
            duration = obj.end_time - obj.start_time
            return int(duration.total_seconds() / 60)
        return 0

class TicketSerializer(serializers.ModelSerializer):
    subscriber = SubscriberSerializer(read_only=True)
    user = SubscriberSerializer(read_only=True)
    ticket_category = TicketCategorySerializer(read_only=True)
    ticket_status = TicketStatusSerializer(read_only=True)
    entries = TicketEntrySerializer(many=True, read_only=True) # Updated this line

    subscriber_id = serializers.PrimaryKeyRelatedField(queryset=Subscriber.objects.all(), source='subscriber', write_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='user', write_only=True, required=False, allow_null=True)
    ticket_category_id = serializers.PrimaryKeyRelatedField(queryset=TicketCategory.objects.all(), source='ticket_category', write_only=True)
    ticket_status_id = serializers.PrimaryKeyRelatedField(queryset=TicketStatus.objects.all(), source='ticket_status', write_only=True)

    class Meta:
        model = Ticket
        fields = [
            'ticket_id', 'opened_on', 'reopened_on', 'closed_on', 'created_at', 'updated_at',
            'subscriber', 'subscriber_id',
            'user', 'user_id',
            'ticket_category', 'ticket_category_id',
            'ticket_status', 'ticket_status_id',
            'entries'
        ]

class UploadSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True)
    circuit = CircuitSerializer(read_only=True)
    home = HomeSerializer(read_only=True)
    subscriber = SubscriberSerializer(read_only=True)
    upload_type = UploadTypeSerializer(read_only=True)

    class Meta:
        model = Uploads
        fields = '__all__'

class UserPermissionSubcategorySerializer(serializers.ModelSerializer):
    category = UserPermissionCategorySerializer(read_only=True)

    class Meta:
        model = UserPermissionSubcategory
        fields = [
            "__all__"
        ]

class UserPermissionTypeSerializer(serializers.ModelSerializer):
    user_permission_category = UserPermissionCategorySerializer(read_only=True)
    user_permission_subcategory = UserPermissionSubcategorySerializer(read_only=True)

    class Meta:
        model = UserPermissionType
        fields = [
            "__all__"
        ]

class UserPermissionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    type = UserPermissionTypeSerializer(read_only=True)
    class Meta:
        model = UserPermissions
        fields = [
          "__all__"
        ]

class UserPermissionDefaultsSerializer(serializers.ModelSerializer):
    UserRole = UserRolesSerializer(read_only=True)
    UserPermissionType = UserPermissionTypeSerializer(read_only=True)

    class Meta:
        model = UserPermissionDefaults
        fields = [
          "__all__"
        ]

class UserProjectsSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    project = ProjectSerializer(read_only=True)
    
    class Meta:
        model = UserProjects
        fields = [
            "__all__"
        ]

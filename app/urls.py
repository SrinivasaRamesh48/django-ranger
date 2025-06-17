from django.urls import path
from app.views.acp_view import SubscriberACPViewSet
from app.views.alerts_view import AlertViewSet
from app.views.alert_types_view import AlertTypesViewSet
from app.views.autopay_view import AutopayViewSet
from app.views.billing_view import SuccessfulTransactionWebhookView
from app.views.circuit_alerts_view import CircuitAlertViewSet
from app.views.circuit_carriers_view import CircuitCarrierViewSet
from app.views.home_alerts_view import HomeAlertViewSet
from app.views.interest_form_view import InterestFormLogViewSet
# from app.views.MacAddressController import MacAddressViewSet
from app.views.node_classes_view import NodeClassViewSet
from app.views.node_frames_view import NodeFrameViewSet
from app.views.nodes_view import NodeViewSet
from app.views.node_types_view import NodeTypeViewSet
from app.views.ont_view import OntViewSet
from app.views.ont_manufacturer_view import OntManufacturerViewSet
from app.views.port_mac_address_view import PortMacAddressViewSet
from app.views.subscriber_alerts_view import SubscriberAlertViewSet
from app.views.subscription_types_view import SubscriptionTypeViewSet
from app.views.ticket_categories_view import TicketCategoryViewSet
from app.views.uploads_view import download_file_view
from app.views.us_states_view import UsStateViewSet
from app.views.user_company_view import UserCompanyViewSet
from app.views.user_roles_view import UserRolesViewSet

urlpatterns = [
    # POST /successful_transaction_webhook -> BillingController@create_transaction
    path('successful_transaction_webhook',SuccessfulTransactionWebhookView.as_view(),name='webhook-successful-transaction'),
    
    
    
    #  ACP
    path('allACP', SubscriberACPViewSet.as_view({'get': 'list'}), name='acp-list'),
    path('acp_enroll', SubscriberACPViewSet.as_view({'post': 'enroll'}), name='acp-enroll'),
    path('cancel_acp_enrollment/<int:pk>', SubscriberACPViewSet.as_view({'put': 'cancel_enrollment'}), name='acp-cancel-enrollment'),
    
    #  System Alerts
    path('alerts', AlertViewSet.as_view({'get': 'list'}), name='alert-list'),
    path('alerts', AlertViewSet.as_view({'post': 'create'}), name='alert-create'),
    path('alerts/<int:alert_id>', AlertViewSet.as_view({'put': 'update'}), name='alert-update'),
    path('alert_types', AlertTypesViewSet.as_view({'get': 'list'}), name='alert-type-list'),
    
    # Circuit Alerts
    path('circuit_alerts', CircuitAlertViewSet.as_view({'post': 'create'}), name='circuit-alert-create'),
    path('circuit_alerts/<int:circuit_alert_id>', CircuitAlertViewSet.as_view({'put': 'update'}), name='circuit-alert-update'),

    # Home Alerts
    path('home_alerts', HomeAlertViewSet.as_view({'post': 'create'}), name='home-alert-create'),
    path('home_alerts/<int:home_alert_id>', HomeAlertViewSet.as_view({'put': 'update'}), name='home-alert-update'),


    # Circuits
    path('circuit_carriers', CircuitCarrierViewSet.as_view({'get': 'list'}), name='circuit-carrier-list'),

    # Statements
    path('allAutopay', AutopayViewSet.as_view({'get': 'list'}), name='autopay-list-all'),

    # Interest Form Logs
    path('interest_form_logs', InterestFormLogViewSet.as_view({'get': 'list'}), name='interest-form-log-list'),

    path('interest_form_logs/<int:interest_form_log_id>', InterestFormLogViewSet.as_view({'put': 'update'}), name='interest-form-log-update'),

    # # MacAddress
    # path('allCPEData', MacAddressViewSet.as_view({'get': 'list'}), name='macaddress-list-all'),
    # path('toggle_firmware_update', MacAddressViewSet.as_view({'post': 'toggle_firmware_update'}), name='macaddress-toggle-firmware'),
    # path('default_cpe_settings/<int:mac_address_id>', MacAddressViewSet.as_view({'get': 'default_cpe_settings'}), name='macaddress-default-settings'),

    # Equipment Page
    path('node_classes', NodeClassViewSet.as_view({'get': 'list'}), name='node-class-list'),
    path('allEquipment', NodeViewSet.as_view({'get': 'list'}), name='equipment-list-all'),
    path('equipment', NodeViewSet.as_view({'post': 'create'}), name='equipment-create'),
    path('equipment/<int:node_id>', NodeViewSet.as_view({'get': 'retrieve'}), name='equipment-detail'),
    path('equipment/<int:node_id>', NodeViewSet.as_view({'put': 'update'}), name='equipment-update'),
    path('node_frames', NodeFrameViewSet.as_view({'get': 'list'}), name='node-frame-list'),
    path('node_types', NodeTypeViewSet.as_view({'get': 'list'}), name='node-type-list'),
    
    #  Networking Page
    path('allONTData', OntViewSet.as_view({'get': 'list'}), name='ont-list-all'),
    
    
    
    #  Other
    path('ont_manufacturers', OntManufacturerViewSet.as_view({'get': 'list'}), name='ont-manufacturer-list'),
    path('download_file/<int:file_id>', download_file_view, name='download-file'),
    path('us_states', UsStateViewSet.as_view({'get': 'list'}), name='us-state-list'),

    #  Networking Page
    path('allPortMacAddressData', PortMacAddressViewSet.as_view({'get': 'list'}), name='port-mac-address-list-all'),

    # subscriber_alerts 
    path('subscriber_alerts', SubscriberAlertViewSet.as_view({'post': 'create'}), name='subscriber-alert-create'),
    path('subscriber_alerts/<int:subscriber_alert_id>', SubscriberAlertViewSet.as_view({'put': 'update'}), name='subscriber-alert-update'),
    
    # projects
     path('subscription_types', SubscriptionTypeViewSet.as_view({'get': 'list'}), name='subscription-type-list'),
     
    #  Ticket 
    path('ticket_categories', TicketCategoryViewSet.as_view({'get': 'list'}), name='ticket-category-list'),
    
    #  User
    path('user_companies', UserCompanyViewSet.as_view({'get': 'list'}), name='user-company-list'),
    path('user_roles', UserRolesViewSet.as_view({'get': 'list'}), name='user-roles-list'),
    
    
    
    ]
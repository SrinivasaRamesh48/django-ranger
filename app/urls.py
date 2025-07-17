from django.urls import path

from app import views
from app.views.register_view import LogoutView,RegisterView,LoginView,FakeGetActiveTicketView,AuthenticateView,ResetMyPasswordView
from app.views.subscriber_view import SubscriberListView
from app.views.acp_view import SubscriberACPViewSet
from app.views.alerts_view import AlertViewSet
from app.views.alert_types_view import AlertTypesViewSet
from app.views.autopay_view import AutopayViewSet
from app.views.billing_view import CreateTransactionWebhookView
from app.views.bulk_message_view import BulkMessageEmailNodesView, BulkMessagePhoneNodesView, BulkMessagePhoneTemplateView, BulkMessageSendEmailsView, BulkMessageSubscriberEmailLogView, BulkMessageSubscriberSMSLogView, BulkMessageView, BulkMessageSendSMSView
from app.views.bulk_message_view import BulkMessageTypesView, BulkMessageNewEmailTemplateView, BulkMessageNewPhoneTemplateView, BulkMessageEditEmailTemplateView, BulkMessageEditPhoneTemplateView, BulkMessageRemoveEmailTemplateView, BulkMessageRemovePhoneTemplateView, BulkMessageEmailTemplateView
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
from app.views.user_view import PermissionTypesView,TechnicianViewSet

urlpatterns = [
    path('allSubscribers', SubscriberListView.as_view(), name='subscriber-list'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('authenticate/', AuthenticateView.as_view(), name='authenticate'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('reset_my_password', ResetMyPasswordView.as_view(), name='reset_my_password'),
    path('active_ticket', FakeGetActiveTicketView.as_view(), name='active_ticket'),
    
    
    # POST /successful_transaction_webhook -> BillingController@create_transaction
    
    
    path('successful_transaction_webhook/', CreateTransactionWebhookView.as_view(), name='successful_transaction_webhook'),
    path('allACP', SubscriberACPViewSet.as_view({'get': 'list'}), name='acp-list'),
    path('acp_enroll', SubscriberACPViewSet.as_view({'post': 'enroll'}), name='acp-enroll'),
    path('cancel_acp_enrollment/<int:pk>', SubscriberACPViewSet.as_view({'put': 'cancel_enrollment'}), name='acp-cancel-enrollment'),

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


    #  Message
    path('bulk_message_email_checkbox_nodes/', BulkMessageEmailNodesView.as_view(), name='bulk-message-email-checkbox-nodes'),
    path('bulk_message_phone_checkbox_nodes/', BulkMessagePhoneNodesView.as_view(), name='bulk-message-phone-checkbox-nodes'),
    path('bulk_message_send_emails/', BulkMessageSendEmailsView.as_view(),name='bulk-message-send-emails'),
    path('bulk_message_send_sms/', BulkMessageSendSMSView.as_view(),name='bulk-message-send-sms'),
    path('bulk_message_subscriber_email_log/<int:id>/', BulkMessageSubscriberEmailLogView.as_view(), name='bulk-message-subscriber-email-log'),
    path('bulk_message_subscriber_sms_log/<int:id>/', BulkMessageSubscriberSMSLogView.as_view(), name='bulk-message-subscriber-sms-log'),
    path('bulk_message_types/', BulkMessageTypesView.as_view(), name='bulk-message-types'),
    path('bulk_message_new_email_template/', BulkMessageNewEmailTemplateView.as_view(), name='bulk-message-new-email-template'),
    path('bulk_message_new_phone_template/', BulkMessageNewPhoneTemplateView.as_view(), name='bulk-message-new-phone-template'),
    path('bulk_message_edit_email_template/', BulkMessageEditEmailTemplateView.as_view(), name='bulk-message-edit-email-template'),
    path('bulk_message_edit_phone_template/', BulkMessageEditPhoneTemplateView.as_view(), name='bulk-message-edit-phone-template'),
    path('bulk_message_remove_email_template/<int:id>/', BulkMessageRemoveEmailTemplateView.as_view(), name='bulk-message-remove-email-template'),
    path('bulk_message_remove_phone_template/<int:id>/', BulkMessageRemovePhoneTemplateView.as_view(), name='bulk-message-remove-phone-template'),
    path('bulk_message_email_template/<int:id>/', BulkMessageEmailTemplateView.as_view(), name='bulk-message-email-template'),
    path('bulk_message_phone_template/<int:id>/', BulkMessagePhoneTemplateView.as_view(), name='bulk-message-phone-template'),
    
    
    # technician
    path('permission-types/', PermissionTypesView.as_view(), name='permission-types'),
    path('technicians/', TechnicianViewSet.as_view({'get': 'list'}), name='technician-list'),
    path('technicians/<int:pk>/',TechnicianViewSet.as_view({'get': 'retrieve', 'put': 'update'}), name='technician-detail'),
    path('technicians/<int:pk>/reset_password/',TechnicianViewSet.as_view({'post': 'reset_password'}), name='technician-reset-password'),
    path('technicians/<int:pk>/update_permissions/',TechnicianViewSet.as_view({'post': 'update_permissions'}), name='technician-update-permissions'),

    ]
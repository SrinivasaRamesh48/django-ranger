from django.urls import path
from app.views.ACPController import SubscriberACPViewSet 
from app.views.AlertsController import AlertViewSet
from app.views.AlertTypesController import AlertTypesViewSet
from app.views.AutopayController import AutopayViewSet
from app.views.BillingController import SuccessfulTransactionWebhookView
from app.views.CircuitAlertsController import CircuitAlertViewSet
from app.views.CircuitCarriersController import CircuitCarrierViewSet
from app.views.HomeAlertsController import HomeAlertViewSet
from app.views.InterestFormController import InterestFormLogViewSet
# from app.views.MacAddressController import MacAddressViewSet
from app.views.NodeClassesController import NodeClassViewSet
from app.views.NodeFramesController import NodeFrameViewSet
from app.views.NodesController import NodeViewSet
from app.views.NodeTypesController import NodeTypeViewSet

urlpatterns = [
    # POST /successful_transaction_webhook -> BillingController@create_transaction
    path(
        'successful_transaction_webhook',
        SuccessfulTransactionWebhookView.as_view(),
        name='webhook-successful-transaction'
    ),
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
    
    
]
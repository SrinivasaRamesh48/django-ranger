from django.urls import path
from app.views.ACPController import SubscriberACPViewSet 
from app.views.AlertsController import AlertViewSet
from app.views.AlertTypesController import AlertTypesViewSet
from app.views.AutopayController import AutopayViewSet
from app.views.BillingController import SuccessfulTransactionWebhookView



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
    
    
    # // Statements
    path('allAutopay', AutopayViewSet.as_view({'get': 'list'}), name='autopay-list-all'),


]
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import BulkEmailTemplateViewSet
from .views import BulkMessageTypeViewSet
from .views import BulkPhoneTemplateViewSet
from .views import CPEControlLogViewSet
router = DefaultRouter()
router.register(r'bulk-email-templates', BulkEmailTemplateViewSet)
router.register(r'bulk-message-types', BulkMessageTypeViewSet)
router.register(r'bulk-phone-templates', BulkPhoneTemplateViewSet)
router.register(r'cpe-control-logs', CPEControlLogViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
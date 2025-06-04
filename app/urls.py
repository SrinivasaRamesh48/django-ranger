from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import BulkEmailTemplateViewSet
from .views import BulkMessageTypeViewSet
from .views import BulkPhoneTemplateViewSet

router = DefaultRouter()
router.register(r'bulk-email-templates', BulkEmailTemplateViewSet)
router.register(r'bulk-message-types', BulkMessageTypeViewSet)
router.register(r'bulk-phone-templates', BulkPhoneTemplateViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
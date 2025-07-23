from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from app.models.user import User
from app.models.user_roles import UserRoles
from app.models.user_company import UserCompany
from app.models.user_permissions import UserPermissions
from app.models.user_permission_type import UserPermissionType
from app.models.subscriber import Subscriber
from app.models.ticket_status import TicketStatus
from app.models.ticket_category import TicketCategory

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    # Optionally, customize list_display, search_fields, etc.
    list_display = ('user_id', 'username', 'email', 'name', 'active', 'activated')
    search_fields = ('username', 'email', 'name')
    ordering = ('user_id',)


@admin.register(UserRoles)
class UserRolesAdmin(admin.ModelAdmin):
    list_display = ('user_role_id', 'description', 'dispatch')
    search_fields = ('description',)


@admin.register(UserCompany)
class UserCompanyAdmin(admin.ModelAdmin):
    list_display = ('user_company_id', 'description')
    search_fields = ('description',)


@admin.register(UserPermissions)
class UserPermissionsAdmin(admin.ModelAdmin):
    list_display = ('user_permission_id', 'user', 'user_permission_type')
    search_fields = ('user__username', 'user_permission_type__identifier')
    list_filter = ('user_permission_type',)


@admin.register(UserPermissionType)
class UserPermissionTypeAdmin(admin.ModelAdmin):
    list_display = ('user_permission_type_id', 'identifier', 'description', 'user_permission_category', 'user_permission_subcategory')
    search_fields = ('identifier', 'description')
    list_filter = ('user_permission_category', 'user_permission_subcategory')


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('subscriber_id', 'username', 'first_name', 'last_name', 'primary_email', 'primary_phone', 'service_activated_on', 'suspended')
    search_fields = ('username', 'first_name', 'last_name', 'primary_email', 'primary_phone')
    list_filter = ('suspended', 'multi_home_subscriber', 'pause_billing', 'service_activated_on')
    readonly_fields = ('subscriber_id', 'password')  # Make ID and password read-only for security
    ordering = ('-subscriber_id',)
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('subscriber_id', 'first_name', 'last_name', 'primary_email', 'username', 'password')
        }),
        ('Contact Information', {
            'fields': ('primary_phone',)
        }),
        ('Service Information', {
            'fields': ('home', 'service_plan', 'node', 'node_port_number', 'service_activated_on', 'service_deactivated_on', 'suspended')
        }),
        ('Billing Information', {
            'fields': ('merchant_customer_id', 'autopay_merchant_id', 'acp_application_id', 'qbo_customer_id', 'pause_billing')
        }),
        ('Multi-Home Settings', {
            'fields': ('multi_home_subscriber',)
        }),
    )


@admin.register(TicketStatus)
class TicketStatusAdmin(admin.ModelAdmin):
    list_display = ('ticket_status_id', 'description')
    search_fields = ('description',)
    ordering = ('ticket_status_id',)


@admin.register(TicketCategory)
class TicketCategoryAdmin(admin.ModelAdmin):
    list_display = ('ticket_category_id', 'description', 'account_portal_visible')
    search_fields = ('description',)
    list_filter = ('account_portal_visible',)
    ordering = ('ticket_category_id',)


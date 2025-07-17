from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from app.models.user import User
from app.models.user_roles import UserRoles
from app.models.user_company import UserCompany
from app.models.user_permissions import UserPermissions
from app.models.user_permission_type import UserPermissionType

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


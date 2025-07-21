from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail  # or your custom mailer
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password
from app.models import User, UserPermissionType, UserPermissions
from app.serializers.user_serializer import UserSerializer
from app.serializers.user_permission_type_serializer import UserPermissionTypeSerializer
import random
import string


class TechnicianViewSet(viewsets.ViewSet):
    def list(self, request):
        users = User.objects.select_related('user_company', 'user_role').all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        user = get_object_or_404(User.objects.select_related(
            'user_company', 'user_role'
        ).prefetch_related(
            'custom_user_permissions__user_permission_type__subcategory__category'
        ), pk=pk)

        permission_ids = [p.user_permission_type.identifier for p in user.custom_user_permissions.all()]
        data = UserSerializer(user).data
        data["permission_identifiers"] = permission_ids
        return Response(data)

    def update(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        for attr, value in request.data.items():
            setattr(user, attr, value)
        user.save()
        return Response({
            "success": True,
            "data": UserSerializer(user).data,
            "message": "User Successfully Updated."
        })

    @action(detail=True, methods=['post'], url_path='reset_password')
    def reset_password(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        user.set_password(password)
        user.activated = False
        user.temp_password = password
        user.save()

        # Send email (custom implementation)
        # send_mail("Your new password", f"Password: {password}", "admin@yourdomain.com", [user.email])

        return Response({
            "success": True,
            "message": "Password Successfully Reset."
        })

    @action(detail=True, methods=['post'], url_path='update_permissions')
    def update_permissions(self, request, pk=None):
        permission_identifiers = request.data.get('permission_identifiers', [])
        user = get_object_or_404(User, pk=pk)

        types = UserPermissionType.objects.filter(identifier__in=permission_identifiers)
        UserPermissions.objects.filter(user=user).delete()
        UserPermissions.objects.bulk_create([
            UserPermissions(user=user, user_permission_type=t) for t in types
        ])

        return Response({
            "success": True,
            "message": "Permissions Successfully Updated."
        })


class PermissionTypesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        results = UserPermissionType.objects.select_related(
            'user_permission_category',
            'user_permission_subcategory'
        ).order_by(
            'user_permission_category_id',
            'user_permission_subcategory_id',
            'description'
        )

        serializer = UserPermissionTypeSerializer(results, many=True)

        return Response({
            'success': bool(results),
            'data': serializer.data,
            'message': "Data Successfully Retrieved." if results else "Failed to Retrieve Data."
        })
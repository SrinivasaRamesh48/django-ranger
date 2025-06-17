# from rest_framework import viewsets, status
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from rest_framework.decorators import action
# from app.models.MacAddress import MacAddress
# from app.serializers.MacAddressSerializer import MacAddress 

# class MacAddressViewSet(viewsets.ReadOnlyModelViewSet):
#     """
#     A ViewSet for viewing and managing MAC Addresses (CPEs).
#     """
#     queryset = MacAddress.objects.all()
#     serializer_class = MacAddressListSerializer
#     permission_classes = [IsAuthenticated]
#     lookup_field = 'mac_address_id'

#     def list(self, request, *args, **kwargs):
#         """Corresponds to the `index` method."""
#         # Eager load related Home and Node data to prevent N+1 queries.
#         queryset = MacAddress.objects.select_related('home', 'home__node').all()
#         serializer = self.get_serializer(queryset, many=True)
#         return Response({
#             'success': True,
#             'data': serializer.data,
#             'message': 'Data Successfully Retrieved.'
#         })

#     @action(detail=False, methods=['post'], url_path='toggle-firmware-update')
#     def toggle_firmware_update(self, request):
#         """Corresponds to the `toggle_firmware_update` method."""
#         mac_id = request.data.get('mac_address_id')
#         firmware_update = request.data.get('firmware_update')
#         firmware_update_manual = request.data.get('firmware_update_manual')

#         if mac_id is None or firmware_update is None or firmware_update_manual is None:
#             return Response({
#                 'success': False,
#                 'message': 'Failed to Toggle Firmware Update. Please contact system administrator'
#             }, status=status.HTTP_400_BAD_REQUEST)

#         updated_count = MacAddress.objects.filter(mac_address_id=mac_id).update(
#             firmware_update=firmware_update,
#             firmware_update_manual=firmware_update_manual
#         )

#         success = updated_count > 0
#         return Response({
#             'success': success,
#             'message': "Successfully Toggled Firmware Update" if success else 'Failed to Toggle Firmware Update. Please contact system administrator'
#         })

#     @action(detail=True, methods=['get'], url_path='default-cpe-settings')
#     def default_cpe_settings(self, request, mac_address_id=None):
#         """Corresponds to the `default_cpe_settings` method."""
#         cpe = self.get_object()

#         if not cpe.default_ssid or not cpe.default_passkey:
#             return Response({
#                 'success': False,
#                 'message': 'Default credentials not found.'
#             }, status=status.HTTP_404_NOT_FOUND)

#         data = cpe.default_credentials()
#         serializer = DefaultCPESettingsSerializer(data)

#         return Response({
#             'success': True,
#             'data': serializer.data,
#             'message': 'Data Successfully Retrieved.'
#         })

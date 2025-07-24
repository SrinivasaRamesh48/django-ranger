# app/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app.models import MacAddress
from app.serializers.mac_address_serializer import MacAddressSerializer
from . import services

class MacAddressListView(APIView):
    def get(self, request):
        try:

            mac_addresses = MacAddress.objects.select_related("home", "home__node").order_by("-mac_address_id")
            serializer = MacAddressSerializer(mac_addresses, many=True)

            response = {
                'success': True,
                'data': serializer.data,
                'message': 'Data Successfully Retrieved.'
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            response = {
                'success': False,
                'data': None,
                'message': f'Failed to Retrieve Data: {str(e)}'
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ToggleFirmwareUpdateView(APIView):
    def post(self, request):
        mac_address_id = request.data.get('mac_address_id')
        firmware_update = request.data.get('firmware_update')
        firmware_update_manual = request.data.get('firmware_update_manual')

        if mac_address_id is None or firmware_update is None or firmware_update_manual is None:
            response = {
                'success': False,
                'message': 'Failed to Toggle Firmware Update. Missing required parameters.'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        try:
            rows_updated = MacAddress.objects.filter(mac_address_id=mac_address_id).update(
                firmware_update=firmware_update,
                firmware_update_manual=firmware_update_manual
            )

            if rows_updated > 0:
                response = {
                    'success': True,
                    'message': "Successfully Toggled Firmware Update"
                }
                return Response(response, status=status.HTTP_200_OK)
            else:
                response = {
                    'success': False,
                    'message': 'Failed to Toggle Firmware Update. MAC Address not found.'
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            response = {
                'success': False,
                'message': f'Failed to Toggle Firmware Update. Please contact system administrator: {str(e)}'
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DefaultCPESettingsView(APIView):
    def get(self, request, pk):
        try:
            cpe = MacAddress.objects.get(pk=pk)
            if not cpe.default_ssid or not cpe.default_passkey:
                response = {
                    'success': False,
                    'data': None,
                    'message': 'Default credentials not found.'
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)

            credentials = cpe.get_default_credentials()

            response = {
                'success': True,
                'data': credentials,
                'message': 'Data Successfully Retrieved.'
            }
            return Response(response, status=status.HTTP_200_OK)

        except MacAddress.DoesNotExist:
            response = {
                'success': False,
                'data': None,
                'message': 'CPE with the specified ID not found.'
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            response = {
                'success': False,
                'data': None,
                'message': f'An error occurred: {str(e)}'
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

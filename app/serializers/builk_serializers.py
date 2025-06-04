from rest_framework import serializers
from app.models.BulkEmailTemplate import BulkEmailTemplate
from app.models.BulkMessageType import BulkMessageType
from app.models.BulkPhoneTemplate import BulkPhoneTemplate

class BulkEmailTemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = BulkEmailTemplate
        fields = '__all__' 
        
class BulkMessageTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BulkMessageType
        fields = '__all__' # This will include all fields from the BulkMessageType model (e.g., bulk_message_type_id, description)

class BulkPhoneTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BulkPhoneTemplate
        fields = '__all__'     


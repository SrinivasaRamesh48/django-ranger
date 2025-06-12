from rest_framework import serializers
from app.models.Alert import Alert
from app.models.AlertType import AlertType



class AlertSerializer(serializers.ModelSerializer):
    """
    This serializer handles the validation and business logic for creating
    and updating Alert objects. This is where the logic from your
    Laravel controller's store() and update() methods now lives.
    """
    class Meta:
        model = Alert
        # We list all fields from the model that we want in the API.
        fields = '__all__'
        # These fields should be set by our business logic, not directly by the client.
        read_only_fields = (
            'alert_id',
            'activated_by',
            'deactivated_by',
            'updated_by',
            'created_at',
            'updated_at'
        )

    def create(self, validated_data):
        """
        This method is called when creating a new Alert (on POST requests).
        It replaces the logic from your `store` method.
        """
        # The user is passed from the view via the context.
        user = self.context['request'].user

        # --- Apply Business Logic ---
        validated_data['activated_by'] = user
        validated_data['updated_by'] = user

        # If the 'active' flag is sent as False on creation, set the deactivator.
        if not validated_data.get('active', True):
            validated_data['deactivated_by'] = user
        else:
            validated_data['deactivated_by'] = None

        # Create and return the new Alert instance.
        return Alert.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        This method is called when updating an existing Alert (on PUT/PATCH requests).
        It replaces the logic from your `update` method.
        `instance` is the original Alert object from the database.
        """
        user = self.context['request'].user

        # --- Apply Business Logic ---
        # Always set the user who performed the update.
        instance.updated_by = user

        # Handle deactivation: only set 'deactivated_by' if the alert is changing
        # from active to inactive.
        is_being_deactivated = 'active' in validated_data and not validated_data['active']
        if is_being_deactivated and instance.active:
            instance.deactivated_by = user

        # Handle re-activation: if the alert is set to active, clear the deactivator.
        is_being_activated = 'active' in validated_data and validated_data['active']
        if is_being_activated:
            instance.deactivated_by = None

        # Manually update the other fields from the validated data.
        instance.alert_type = validated_data.get('alert_type', instance.alert_type)
        instance.message = validated_data.get('message', instance.message)
        instance.active = validated_data.get('active', instance.active)
        # Add any other fields that can be updated here.

        instance.save()
        return instance
        
        
class AlertTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertType
        fields = '__all__'         
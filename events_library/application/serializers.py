from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from ..core.event_bus import CudEvent


class EventSerializer(serializers.Serializer):
    """Serializer for validating payloads in any event"""
    event_type = serializers.CharField()
    payload = serializers.JSONField()


class CudPayloadSerializer(serializers.Serializer):
    """Serializer for validating payloads in CUD events"""
    id = serializers.UUIDField()
    cud_operation = serializers.CharField()
    data = serializers.JSONField()
    timestamp = serializers.FloatField()

    class Meta:
        fields = '__all__'

    def validate_cud_operation(self, value):
        if value not in [
            CudEvent.CREATED, CudEvent.UPDATED, CudEvent.DELETED,
        ]:
            raise ValidationError({
                'cud_operation: 'f'{value} is not a valid value'
            })
        return value

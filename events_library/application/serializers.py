from rest_framework import serializers


class EventSerializer(serializers.Serializer):
    """Serializer for validating payloads in any event"""
    event_type = serializers.CharField()
    payload = serializers.JSONField()


class CudPayloadSerializer(serializers.Serializer):
    """Serializer for validating payloads in CUD events"""
    id = serializers.UUIDField()
    cud_operation = serializers.CharField()
    data = serializers.JSONField(),
    timestamp = serializers.DateTimeField()

    class Meta:
        fields = '__all__'

    def validate_cud_operation(self, value):
        return value in ['created', 'updated', 'deleted']

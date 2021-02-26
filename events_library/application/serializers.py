from rest_framework import serializers


class EventSerializer(serializers.Serializer):
    event_type = serializers.CharField()
    payload = serializers.JSONField()


class CudPayloadSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    cud_operation = serializers.CharField()
    data = serializers.JSONField(),
    timestamp = serializers.DateTimeField()

    class Meta:
        fields = '__all__'

    def validate_cud_operation(self, value):
        return value in ['created', 'updated', 'deleted']

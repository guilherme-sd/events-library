from rest_framework import serializers


class EventSerializer(serializers.Serializer):
    event_type = serializers.CharField()
    payload = serializers.JSONField()

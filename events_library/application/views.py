from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.status import HTTP_204_NO_CONTENT

from jwt_auth.authentication import ServiceTokenAuthentication

from events_library.application.permissions import ServiceTokenPermission
from events_library.application.serializers import (
    EventSerializer, CudPayloadSerializer,
)
from events_library.core.event_bus import EventBus


class EventViewSet(ViewSet):
    """Viewset for handling handling emitted events"""
    authentication_classes = [ServiceTokenAuthentication]
    permission_classes = [ServiceTokenPermission]

    @action(detail=False, methods=['post'], url_path='event')
    def handle_event(self, request: Request):
        event_serializer = EventSerializer(data=request.data)
        event_serializer.is_valid(raise_exception=True)

        event_type = event_serializer.validated_data['event_type']
        payload = event_serializer.validated_data['payload']

        payload_serializer = CudPayloadSerializer(data=payload)
        if payload_serializer.is_valid():
            EventBus.emit_cud_locally(event_type, payload)
        else:
            EventBus.emit_locally(event_type, payload)

        return Response(status=HTTP_204_NO_CONTENT)

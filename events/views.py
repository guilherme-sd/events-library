

from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.status import HTTP_204_NO_CONTENT


from jwt_auth.authentication import ServiceTokenAuthentication

from .event_bus import EventBus
from .permissions import ServiceTokenPermission
from .serializers import EventSerializer


class EventViewSet(ViewSet):
    authentication_classes = [ServiceTokenAuthentication]
    permission_classes = [ServiceTokenPermission]

    @action(detail=False, methods=['post'], url_path='/')
    def handle_event(self, request: Request):
        serializer = EventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        event_type = serializer.validated_data['event_type']
        payload = serializer.validated_data['payload']

        EventBus.emit_locally(event_type, payload)

        return Response(status=HTTP_204_NO_CONTENT)

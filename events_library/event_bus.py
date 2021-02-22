
import typing
from django.conf import settings
from .api import BaseApi

EVENTS_MAPPING = settings.EVENTS_MAPPING
EVENTS_URL = settings.EVENTS_URL


class EventBus():
    subscribers = {}

    @classmethod
    def subscribe(cls, event_type: str, event_handler: typing.Callable):
        # Get current list of handlers
        event_handlers = cls.subscribers.get(event_type, [])
        # Add the new handler
        event_handlers.append(event_handler)

        cls.subscribers[event_type] = event_handlers

    @classmethod
    def emit_locally(cls, event_type: str, payload: typing.Dict):
        if event_type not in cls.subscribers:
            return  # No op

        for event_handler in cls.subscribers[event_type]:
            event_handler(payload)

    @classmethod
    def emit_abroad(cls, event_type: str, payload: typing.Dict):
        if event_type not in EVENTS_MAPPING:
            return  # No op

        api = BaseApi()

        for service in EVENTS_MAPPING[event_type]:
            path = f'{service}/{EVENTS_URL}/'
            api.send_request(path, payload)

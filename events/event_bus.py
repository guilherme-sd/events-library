
import typing
from django.conf import settings
from .api import BaseApi

EVENTS_MAPPING = settings.EVENTS_MAPPING
EVENTS_URL = settings.EVENTS_URL


class EventBus():
    def __init__(self):
        self.subscribers = {}
        self.target_services = EVENTS_MAPPING

    @classmethod
    def subscribe(self, event_type: str, event_handler: typing.Callable):
        current_handlers = self.subscribers.get(event_type, [])
        current_handlers.append(event_handler)

    @classmethod
    def emit_locally(self, event_type: str, payload: typing.Dict):
        if event_type not in self.subscribers:
            return  # No op

        for event_handler in self.subscribers[event_type]:
            event_handler(payload)

    @classmethod
    def emit_abroad(self, event_type: str, payload: typing.Dict):
        if event_type not in self.target_services:
            return  # No op

        api = BaseApi()

        for service in self.target_services[event_type]:
            path = f'{service}/{EVENTS_URL}/'
            api.send_request(path, payload, True)

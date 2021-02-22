
import typing
from django.conf import settings
from .api import BaseApi

EVENTS_MAPPING = settings.EVENTS_MAPPING
EVENTS_URL = settings.EVENTS_URL


class EventBus():
    # A mapping, where the key is an event_type,
    # and the value is a list of event_handlers
    event_subscribers = {}

    @classmethod
    def subscribe(cls, event_type: str, event_handler: typing.Callable):
        """Adds the event_handler to the list of functions to be
        called when an event with the given event_type is emitted"""
        # Get current list of handlers
        event_handlers = cls.event_subscribers.get(event_type, [])

        # Add the new handler
        event_handlers.append(event_handler)
        cls.event_subscribers[event_type] = event_handlers

    @classmethod
    def emit_locally(cls, event_type: str, payload: typing.Dict):
        """Calls, with the given payload as argument, each
        event_handler that was attached to the given event_type"""
        if event_type not in cls.event_subscribers:
            return  # No op

        for event_handler in cls.event_subscribers[event_type]:
            event_handler(payload)

    @classmethod
    def emit_abroad(cls, event_type: str, payload: typing.Dict):
        """Sends the event to the services that were set (in the devops
        submodule settings) as 'subscribed' to the given event_type"""
        if event_type not in EVENTS_MAPPING:
            return  # No op

        api = BaseApi()

        for service_name in EVENTS_MAPPING[event_type]:
            path = f'service/{service_name}/{EVENTS_URL}/'
            api.send_request(path, payload)

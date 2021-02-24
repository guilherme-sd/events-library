
import typing
from django.conf import settings

from .api import BaseApi
from .models.handler_log import HandlerLog

EVENTS_MAPPING = settings.EVENTS_MAPPING


class EventBus():
    """Main class of the lib, controlling the
    event's logic and subscription/emittion flow"""

    # A mapping, where the key is an event_type,
    # and the value is a list of event_handlers
    map_event_to_handlers = {}

    # A mapping, where the key is an event_type,
    # and the value is a list of service's names
    map_event_to_subscribers = {}

    @classmethod
    def subscribe(cls, event_type: str, event_handler: typing.Callable):
        """Adds the event_handler to the list of functions to be
        called when an event with the given event_type is emitted"""
        # Get current list of handlers
        event_handlers = cls.map_event_to_handlers.get(event_type, [])

        # Add the new handler
        event_handlers.append(event_handler)
        cls.map_event_to_handlers[event_type] = event_handlers

    @classmethod
    def emit_locally(cls, event_type: str, payload: typing.Dict):
        """Calls, with the given payload as argument, each
        event_handler that was attached to the given event_type.
        It creates a HandlerLog in case of Exception during the
        execution of a handler funtion"""
        if event_type not in cls.map_event_to_handlers:
            return  # No op

        for event_handler in cls.map_event_to_handlers[event_type]:
            try:
                event_handler(payload)

            except Exception as error:
                HandlerLog.objects.create(
                    event_type=event_type,
                    payload=payload,
                    error_message=str(error),
                    handler_name=str(event_handler),
                )

    @classmethod
    def emit_abroad(cls, event_type: str, payload: typing.Dict):
        """Sends the event to the services that
        are subscribed to the given event_type"""
        if event_type not in cls.map_event_to_subscribers:
            return  # No op

        api = BaseApi()

        for service_name in cls.map_event_to_subscribers[event_type]:
            api.send_event_request(service_name, event_type, payload)

    @classmethod
    def declare_event(
        cls,
        event_type: str,
        subscribed_services: typing.List[str]
    ):
        """Registers the services that should receive
        the events with the given event_type"""
        pass

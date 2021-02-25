
import typing

from events_library.core.event_api import EventApi
from events_library.models.handler_log import HandlerLog


class EventBus():
    """Main class of the lib, controlling the
    event's logic and subscription/emittion flow"""

    # A mapping, where the key is an event_type,
    # and the value is a list of event_handlers
    map_event_to_handlers = {}

    # A mapping, where the key is an event_type,
    # and the value is a list of service's names
    map_event_to_target_services = {}

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
        if event_type not in cls.map_event_to_target_services:
            return  # No op

        api = EventApi()

        for target_service in cls.map_event_to_target_services[event_type]:
            api.send_event_request(target_service, event_type, payload)

    @classmethod
    def declare_event(
        cls,
        event_type: str,
        target_services: typing.List[str]
    ):
        """Registers the services that should receive
        the events with the given event_type"""
        current_targets = cls.map_event_to_target_services.get(event_type, [])

        for service_name in target_services:
            if service_name not in current_targets:
                current_targets.append(service_name)

        cls.map_event_to_target_services[event_type] = current_targets

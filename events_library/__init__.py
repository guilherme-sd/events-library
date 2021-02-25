import typing
from typing import Callable, Union

from .constants import Service  # noqa: F401
from .event_bus import EventBus
from .application.views import EventViewSet  # noqa: F401


def emit(event_type: str, payload: typing.Dict):
    """Sends the payload to the services
    that are subscribed to that event_type

    Arguments:
        event_type: str
            The type of the event that will be emitted
        payload: dict
            The data sent along the event
    """
    EventBus.emit_abroad(event_type, payload)


def subscribe_to(
    event_type: str,
    event_handler: Union[Callable, typing.List[Callable]],
):
    """Performs the required configuration so that when an
    event with the given event_type is emitted, the event_handler
    functions are call using the payload of the event as argument

    Arguments:
        event_type: str
            The type of the event that you want to subscribe to

        event_handler: list | Callable
            The function or list of functions that should
            be called when the event is emitted. The functions
            should receive a single argument: the payload, which
            is a dict object
    """
    if isinstance(event_handler, list):
        for handler in event_handler:
            EventBus.subscribe(event_type, handler)
    else:
        EventBus.subscribe(event_type, event_handler)


def declare_event(
    event_type: str,
    subscribed_services: typing.List[str],
):
    """Configures that events of the given event_type
    reach the services provided in the subscribed_services
    argument (even if they didn't subscribed to the event).
    NOTE: This function should not be called more than once
    for each event_type: you might be doing something wrong

    Arguments:
        event_type: str
            The type of the event that you want to subscribe to

        subscribed_services: List[str]
            The names of the services that are subscribed to that
            event_type.

    NOTE:
    Admisable values for the service names are:

    - 'accounts'
    - 'orders'
    - 'payments'
    - 'profiles'
    - 'reports'
    - 'selfdecode'

    You can use the Service class (exported from the events_library
    as well) for getting those options and avoid errors
    """
    for service_name in subscribed_services:
        if Service.not_a_service_option(service_name):
            raise ValueError(
                f'{service_name} is not allowed '
                'as a member of subscribed_services'
            )

    EventBus.declare_event(event_type, subscribed_services)

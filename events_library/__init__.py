import typing
from typing import Callable, Union
from .event_bus import EventBus


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

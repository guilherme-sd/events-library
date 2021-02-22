import typing
from .event_bus import EventBus


def emit(event_type: str, payload: typing.Dict):
    EventBus.emit_abroad(event_type, payload)


def subscribe_to(event_type, event_handler: typing.Callable):
    EventBus.subscribe(event_type, event_handler)

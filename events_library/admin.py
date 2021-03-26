import typing

from django.contrib import admin
from django.db.models import Model
from django.http.request import HttpRequest
from enumfields.admin import EnumFieldListFilter

from .domain import EventLog, HandlerLog


class InmutableAdminModel(admin.ModelAdmin):
    """Admin model class that disables the
    Add and Edit functionalities of the model,
    although it still allows the deletion"""

    def has_add_permission(self, request: HttpRequest) -> bool:
        """Disables Add"""
        return False

    def has_change_permission(
        self,
        request: HttpRequest,
        obj: typing.Optional[Model] = None,
    ) -> bool:
        """Disables Edit"""
        return False


@admin.register(EventLog)
class EventLogAdmin(InmutableAdminModel):
    list_filter = [
        "was_success",
        "event_type",
        ("target_service", EnumFieldListFilter),
    ]
    list_display = [
        'id', 'event_type', 'target_service',
        'was_success', 'created_at',
    ]
    ordering = ["-created_at"]


@admin.register(HandlerLog)
class HandlerLogAdmin(InmutableAdminModel):
    list_filter = ["event_type", "handler_name"]

    list_display = [
        'id', 'event_type', 'handler_name', 'created_at',
    ]
    ordering = ["-created_at"]

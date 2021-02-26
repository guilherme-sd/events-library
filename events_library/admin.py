import typing

from django.contrib import admin
from django.db.models import Model
from django.http.request import HttpRequest

from events_library.models import EventLog, HandlerLog


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


# Register your models here.
admin.site.register(EventLog, InmutableAdminModel)
admin.site.register(HandlerLog, InmutableAdminModel)

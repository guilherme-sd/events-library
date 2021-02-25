import typing

from django.contrib import admin
from django.db.models import Model
from django.http.request import HttpRequest

from events_library.models import EventLog, HandlerLog


class InmutableAdminModel(admin.ModelAdmin):
    def has_add_permission(self, request: HttpRequest) -> bool:
        return False

    def has_change_permission(
        self,
        request: HttpRequest,
        obj: typing.Optional[Model] = None,
    ) -> bool:
        return False


# Register your models here.
admin.site.register(EventLog, InmutableAdminModel)
admin.site.register(HandlerLog, InmutableAdminModel)

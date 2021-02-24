"""Implements the ServiceTokenPermission class"""
import typing

from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from django.views import View


class ServiceTokenPermission(BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:
        if request.auth is None:
            return False

        try:
            return 'Service' in request.user.groups
        except KeyError:
            return False

    def has_object_permission(
        self, request: Request, view: View, obj: typing.Any,
    ) -> bool:
        return False  # pragma: no coverage

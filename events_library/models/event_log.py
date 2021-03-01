from django.contrib.postgres.fields import JSONField
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models

from .base import BaseModel


class EventLog(BaseModel):
    target_service = models.CharField(max_length=20, editable=False)
    event_type = models.CharField(max_length=60, blank=False)
    payload = JSONField(default=dict, encoder=DjangoJSONEncoder)

    retry_number = models.IntegerField(default=0)
    was_success = models.BooleanField(default=False)
    error_message = models.TextField(blank=True)

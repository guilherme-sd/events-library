from django.db import models
from .base import BaseModel

from django.contrib.postgres.fields import JSONField


class HandlerLog(BaseModel):
    handler_name = models.CharField(max_length=60)
    error_message = models.TextField()

    event_type = models.CharField(max_length=60, blank=False)
    payload = JSONField(default=dict)

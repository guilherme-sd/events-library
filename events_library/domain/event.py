

from django.db import models
from .base import BaseModel

from django.contrib.postgres.fields import JSONField


class EventLog(BaseModel):

    event_type = models.CharField(blank=False)
    payload = JSONField(default=dict)
    target_service = models.CharField(editable=False)

    retries = models.IntegerField(default=0)
    success = models.BooleanField(default=False)

    class Meta:
        abstract = True

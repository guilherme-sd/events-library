from django.contrib.postgres.fields import JSONField
from django.db import models
from uuid import uuid4


class BaseModel(models.Model):
    """Common primary key abstract model class"""
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ObjectModel(models.Model):
    """Model class to be used as argument in declare_cud_event"""
    id = models.TextField(primary_key=True, null=False)

    data = JSONField()
    timestamp = models.FloatField()

    class Meta:
        abstract = True

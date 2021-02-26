from django.contrib.postgres.fields import JSONField
from django.db import models
from uuid import uuid4


class BaseModel(models.Model):
    """Common primary key abstract model class, 
    with created_at and updated_at fields included"""
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ObjectModel(models.Model):
    """Model class to be used for replicating
    models in other services and synchronization"""
    id = models.TextField(primary_key=True, null=False)

    data = JSONField()
    timestamp = models.FloatField()

    class Meta:
        abstract = True

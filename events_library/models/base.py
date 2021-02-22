from uuid import uuid4
from django.db import models


class BaseModel(models.Model):
    """Common primary key abstract model class"""

    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta class"""
        abstract = True

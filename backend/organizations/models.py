import uuid
from django.db import models

class Organization(models.Model):
    """
    Represents a multi-tenant organization using the platform.
    All ESG records belong to an Organization.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True, help_text="Enterprise name")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

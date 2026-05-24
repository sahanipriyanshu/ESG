import uuid
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.serializers.json import DjangoJSONEncoder

class AuditLog(models.Model):
    """
    Tracks all mutations and workflow actions across the system.
    Using GenericForeignKey allows us to attach logs to RawRecord, NormalizedRecord, or DataSource.
    """
    class Action(models.TextChoices):
        CREATE = 'create', 'Create'
        UPDATE = 'update', 'Update'
        DELETE = 'delete', 'Delete'
        LOCK = 'lock', 'Lock'
        APPROVE = 'approve', 'Approve'
        REJECT = 'reject', 'Reject'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Generic Relation fields
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=255) # Use CharField to support UUIDs as strings
    content_object = GenericForeignKey('content_type', 'object_id')
    
    action = models.CharField(max_length=20, choices=Action.choices)
    
    # The state changes
    previous_values = models.JSONField(null=True, blank=True, help_text="State before the action", encoder=DjangoJSONEncoder)
    new_values = models.JSONField(null=True, blank=True, help_text="State after the action", encoder=DjangoJSONEncoder)
    
    # User who performed the action (for a real app, this would be a ForeignKey to User)
    # Using a CharField for prototype simplicity, but representing the "actor"
    actor = models.CharField(max_length=255, default='system', help_text="User ID or System process")
    
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action.upper()} on {self.content_type.model} ({self.timestamp.strftime('%Y-%m-%d %H:%M:%S')})"

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['timestamp']),
        ]

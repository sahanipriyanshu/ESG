import uuid
from django.db import models
from organizations.models import Organization

class DataSource(models.Model):
    """
    Represents an ingestion source (e.g., an uploaded CSV file or an API payload).
    """
    class SourceType(models.TextChoices):
        SAP = 'sap', 'SAP'
        UTILITY = 'utility', 'Utility'
        TRAVEL = 'travel', 'Travel'
        OTHER = 'other', 'Other'

    class IngestionMode(models.TextChoices):
        BATCH = 'batch', 'Batch Upload'
        API = 'api', 'API Integration'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='data_sources')
    source_type = models.CharField(max_length=50, choices=SourceType.choices)
    ingestion_mode = models.CharField(max_length=20, choices=IngestionMode.choices)
    original_file = models.FileField(upload_to='uploads/%Y/%m/%d/', null=True, blank=True, help_text="Retained for auditability")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_source_type_display()} - {self.organization.name} ({self.uploaded_at.strftime('%Y-%m-%d')})"

    class Meta:
        ordering = ['-uploaded_at']


class RawRecord(models.Model):
    """
    Immutable storage of the original data row exactly as received.
    If the format changes or normalization logic bugs out, we can replay from here.
    """
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending Normalization'
        PROCESSED = 'processed', 'Successfully Processed'
        FAILED = 'failed', 'Processing Failed'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    data_source = models.ForeignKey(DataSource, on_delete=models.CASCADE, related_name='raw_records')
    raw_payload = models.JSONField(help_text="The exact key-value pairs from the source row/API")
    ingestion_status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    error_message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"RawRecord {self.id} ({self.get_ingestion_status_display()})"


class NormalizedRecord(models.Model):
    """
    The canonical, standardized ESG record ready for reporting and analyst review.
    """
    class RecordStatus(models.TextChoices):
        PENDING_REVIEW = 'pending_review', 'Pending Analyst Review'
        APPROVED = 'approved', 'Approved'
        REJECTED = 'rejected', 'Rejected'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='normalized_records')
    raw_record = models.OneToOneField(RawRecord, on_delete=models.CASCADE, related_name='normalized_record')
    
    # Classification
    category = models.CharField(max_length=100, help_text="e.g., stationary_combustion, purchased_electricity")
    scope = models.IntegerField(choices=[(1, 'Scope 1'), (2, 'Scope 2'), (3, 'Scope 3')])
    
    # Normalized Data
    activity_date = models.DateField(help_text="The actual date or start date of the activity")
    quantity = models.DecimalField(max_digits=19, decimal_places=4)
    normalized_unit = models.CharField(max_length=50, help_text="Standardized unit (e.g., kWh, kg, km)")
    estimated_emissions = models.DecimalField(max_digits=19, decimal_places=4, null=True, blank=True, help_text="Calculated CO2e in kg")
    
    # Review Workflow
    status = models.CharField(max_length=20, choices=RecordStatus.choices, default=RecordStatus.PENDING_REVIEW)
    suspicious_reason = models.TextField(null=True, blank=True, help_text="Why the system flagged this record")
    locked_for_audit = models.BooleanField(default=False, help_text="If True, no further edits allowed")
    
    # Metadata
    source_of_truth = models.CharField(max_length=100, help_text="Origin system identifier (e.g., SAP_ERP_01)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.category} - {self.quantity} {self.normalized_unit} ({self.organization.name})"

    class Meta:
        ordering = ['-activity_date']
        indexes = [
            models.Index(fields=['organization', 'status']),
            models.Index(fields=['scope', 'category']),
        ]

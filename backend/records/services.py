from django.db import transaction
from django.forms.models import model_to_dict
from audit.models import AuditLog
from .models import NormalizedRecord

class RecordWorkflowService:
    @staticmethod
    @transaction.atomic
    def approve_record(record: NormalizedRecord, actor: str) -> NormalizedRecord:
        if record.locked_for_audit:
            raise ValueError("Record is locked and cannot be modified.")
            
        previous_state = model_to_dict(record)
        
        record.status = NormalizedRecord.RecordStatus.APPROVED
        record.save()
        
        new_state = model_to_dict(record)
        
        AuditLog.objects.create(
            content_object=record,
            action=AuditLog.Action.APPROVE,
            previous_values=previous_state,
            new_values=new_state,
            actor=actor
        )
        return record

    @staticmethod
    @transaction.atomic
    def reject_record(record: NormalizedRecord, actor: str, reason: str = None) -> NormalizedRecord:
        if record.locked_for_audit:
            raise ValueError("Record is locked and cannot be modified.")
            
        previous_state = model_to_dict(record)
        
        record.status = NormalizedRecord.RecordStatus.REJECTED
        if reason:
            record.suspicious_reason = f"Rejected: {reason}"
        record.save()
        
        new_state = model_to_dict(record)
        
        AuditLog.objects.create(
            content_object=record,
            action=AuditLog.Action.REJECT,
            previous_values=previous_state,
            new_values=new_state,
            actor=actor
        )
        return record

    @staticmethod
    @transaction.atomic
    def lock_record(record: NormalizedRecord, actor: str) -> NormalizedRecord:
        if record.status != NormalizedRecord.RecordStatus.APPROVED:
            raise ValueError("Only approved records can be locked.")
        if record.locked_for_audit:
            return record # Already locked
            
        previous_state = model_to_dict(record)
        
        record.locked_for_audit = True
        record.save()
        
        new_state = model_to_dict(record)
        
        AuditLog.objects.create(
            content_object=record,
            action=AuditLog.Action.LOCK,
            previous_values=previous_state,
            new_values=new_state,
            actor=actor
        )
        return record

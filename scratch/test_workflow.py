import os
import django
import sys

# Setup Django environment
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from rest_framework.test import APIRequestFactory
from rest_framework import status

from records.models import NormalizedRecord
from audit.models import AuditLog
from records.views import RecordApproveView, RecordRejectView, RecordLockView, NormalizedRecordListView
from audit.views import AuditLogListView

def run_tests():
    factory = APIRequestFactory()
    
    print("\n--- Testing Analyst Workflow ---")
    
    # Get a pending record
    record = NormalizedRecord.objects.filter(status=NormalizedRecord.RecordStatus.PENDING_REVIEW).first()
    if not record:
        print("No pending records found to test workflow. Run test_ingestion.py first.")
        return
        
    print(f"Testing on Record: {record.id} ({record.category})")
    
    # 1. Test List APIs (suspicious)
    request = factory.get('/api/records/?suspicious=true')
    view = NormalizedRecordListView.as_view()
    response = view(request)
    print(f"Suspicious Records Count: {len(response.data)}")
    
    # 2. Approve Record
    print(f"\nApproving record {record.id}...")
    request = factory.post(f'/api/records/{record.id}/approve/', {'actor': 'Analyst Alice'}, format='json')
    view = RecordApproveView.as_view()
    response = view(request, pk=record.id)
    print(f"Approve Status: {response.status_code}")
    
    # 3. Lock Record
    print(f"Locking record {record.id}...")
    request = factory.post(f'/api/records/{record.id}/lock/', {'actor': 'Manager Bob'}, format='json')
    view = RecordLockView.as_view()
    response = view(request, pk=record.id)
    print(f"Lock Status: {response.status_code}")
    
    # 4. Attempt to reject locked record (should fail)
    print(f"Attempting to reject locked record {record.id}...")
    request = factory.post(f'/api/records/{record.id}/reject/', {'actor': 'Analyst Alice'}, format='json')
    view = RecordRejectView.as_view()
    response = view(request, pk=record.id)
    print(f"Reject Locked Record Status: {response.status_code} (Expected 400)")
    
    # 5. Fetch Audit Trail
    print(f"\nFetching audit trail for record {record.id}...")
    request = factory.get(f'/api/audit/?record_id={record.id}')
    view = AuditLogListView.as_view()
    response = view(request)
    print(f"Audit Trail Count: {len(response.data)}")
    for audit in response.data:
        print(f" - [{audit['timestamp']}] {audit['actor']} performed {audit['action']}")

if __name__ == "__main__":
    run_tests()

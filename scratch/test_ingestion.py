import os
import django
import sys
import json
from django.core.files.uploadedfile import SimpleUploadedFile

# Setup Django environment
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from organizations.models import Organization
from records.models import DataSource, RawRecord, NormalizedRecord
from ingestion.serializers import FileUploadSerializer, TravelPayloadSerializer
from ingestion.services.sap_service import SAPService
from ingestion.services.utility_service import UtilityService
from ingestion.services.travel_service import TravelService

def run_tests():
    # 1. Create Organization
    org, created = Organization.objects.get_or_create(name="Acme Corp Test")
    print(f"Using Organization: {org.name} (ID: {org.id})")

    # 2. Test SAP Service
    print("\n--- Testing SAP Ingestion ---")
    sap_service = SAPService(org)
    with open('../scratch/sap_sample.csv', 'rb') as f:
        file_obj = SimpleUploadedFile("sap_sample.csv", f.read(), content_type="text/csv")
        result = sap_service.process(file_obj)
        print("SAP Process Result:", result)

    # 3. Test Utility Service
    print("\n--- Testing Utility Ingestion ---")
    utility_service = UtilityService(org)
    with open('../scratch/utility_sample.csv', 'rb') as f:
        file_obj = SimpleUploadedFile("utility_sample.csv", f.read(), content_type="text/csv")
        result = utility_service.process(file_obj)
        print("Utility Process Result:", result)

    # 4. Test Travel Service
    print("\n--- Testing Travel Ingestion ---")
    travel_payloads = [
        {"type": "flight", "date": "2023-04-10", "origin": "JFK", "destination": "LHR"},
        {"type": "flight", "date": "2023-04-12", "distance": 800},
        {"type": "hotel", "date": "2023-04-10", "nights": 5},
        {"type": "hotel", "date": "2023-04-15", "nights": 40},
        {"type": "ground", "date": "2023-04-15", "distance": -10}
    ]
    travel_service = TravelService(org)
    result = travel_service.process(travel_payloads)
    print("Travel Process Result:", result)

    # 5. Check Database
    print("\n--- Database Summary ---")
    print(f"DataSources: {DataSource.objects.count()}")
    print(f"RawRecords: {RawRecord.objects.count()} (Failed: {RawRecord.objects.filter(ingestion_status='failed').count()})")
    print(f"NormalizedRecords: {NormalizedRecord.objects.count()} (Suspicious: {NormalizedRecord.objects.exclude(suspicious_reason__isnull=True).exclude(suspicious_reason='').count()})")

    for nr in NormalizedRecord.objects.all():
        print(f"  [{nr.category}] {nr.quantity} {nr.normalized_unit} | Suspicious: {nr.suspicious_reason}")

if __name__ == "__main__":
    run_tests()

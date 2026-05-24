from decimal import Decimal
from datetime import datetime
from django.db import transaction
from records.models import DataSource, RawRecord, NormalizedRecord
from .base import BaseIngestionService

# Mock distance lookup (in km)
AIRPORT_DISTANCES = {
    ('JFK', 'LHR'): 5540,
    ('LHR', 'JFK'): 5540,
    ('SFO', 'JFK'): 4150,
    ('JFK', 'SFO'): 4150,
    ('FRA', 'LHR'): 650,
    ('LHR', 'FRA'): 650,
}

class TravelService(BaseIngestionService):
    @property
    def source_type(self):
        return DataSource.SourceType.TRAVEL

    def process(self, payloads):
        """
        Expects a list of dictionaries (JSON payload from API).
        """
        data_source = self.create_data_source(file_obj=None)
        
        if not isinstance(payloads, list):
            payloads = [payloads]

        records_created = 0
        with transaction.atomic():
            for raw_payload in payloads:
                raw_record = RawRecord.objects.create(
                    data_source=data_source,
                    raw_payload=raw_payload,
                    ingestion_status=RawRecord.Status.PENDING
                )
                
                try:
                    self._normalize_and_save(raw_record, raw_payload)
                    raw_record.ingestion_status = RawRecord.Status.PROCESSED
                    raw_record.save()
                    records_created += 1
                except Exception as e:
                    raw_record.ingestion_status = RawRecord.Status.FAILED
                    raw_record.error_message = str(e)
                    raw_record.save()
        
        return {"status": "success", "records_processed": records_created}

    def _normalize_and_save(self, raw_record, payload):
        """
        Simulate flight, hotel, ground transport
        Fields: type (flight/hotel/ground), date, distance (optional), origin, destination, nights (for hotel)
        """
        travel_type = payload.get('type', 'unknown').lower()
        date_str = payload.get('date')
        
        try:
            activity_date = datetime.strptime(str(date_str), "%Y-%m-%d").date()
        except (ValueError, TypeError):
             raise ValueError("Invalid date format. Expected YYYY-MM-DD")

        quantity = Decimal('0')
        normalized_unit = 'km'
        suspicious_reasons = []
        
        if travel_type == 'flight':
            distance = payload.get('distance')
            if not distance:
                origin = str(payload.get('origin', '')).upper()
                dest = str(payload.get('destination', '')).upper()
                distance = AIRPORT_DISTANCES.get((origin, dest), 1000) # fallback to 1000km
                if (origin, dest) not in AIRPORT_DISTANCES:
                    suspicious_reasons.append(f"Estimated distance used for {origin}-{dest}.")
            
            quantity = Decimal(str(distance))
            # Mock emission factor for flight: ~0.15 kg CO2e / km
            emission_factor = Decimal('0.15')
            
        elif travel_type == 'hotel':
            nights = payload.get('nights', 1)
            quantity = Decimal(str(nights))
            normalized_unit = 'nights'
            # Mock emission factor: ~15 kg CO2e / night
            emission_factor = Decimal('15.0')
            if quantity > 30:
                suspicious_reasons.append("Hotel stay > 30 nights.")
                
        elif travel_type == 'ground':
            distance = payload.get('distance', 0)
            quantity = Decimal(str(distance))
            # Mock emission factor: ~0.2 kg CO2e / km
            emission_factor = Decimal('0.2')
        else:
            raise ValueError(f"Unknown travel type: {travel_type}")

        if quantity <= 0:
            suspicious_reasons.append(f"Zero or negative quantity for {travel_type}.")

        estimated_emissions = quantity * emission_factor

        NormalizedRecord.objects.create(
            organization=self.organization,
            raw_record=raw_record,
            category="business_travel",
            scope=3,
            activity_date=activity_date,
            quantity=quantity,
            normalized_unit=normalized_unit,
            estimated_emissions=estimated_emissions,
            status=NormalizedRecord.RecordStatus.PENDING_REVIEW,
            suspicious_reason=" | ".join(suspicious_reasons) if suspicious_reasons else None,
            source_of_truth="TRAVEL_API"
        )

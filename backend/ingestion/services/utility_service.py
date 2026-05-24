import pandas as pd
from decimal import Decimal
from datetime import datetime
from django.db import transaction
from records.models import DataSource, RawRecord, NormalizedRecord
from .base import BaseIngestionService

class UtilityService(BaseIngestionService):
    @property
    def source_type(self):
        return DataSource.SourceType.UTILITY

    def process(self, file_obj):
        data_source = self.create_data_source(file_obj=file_obj)
        file_obj.seek(0)
        
        try:
            df = pd.read_csv(file_obj)
        except Exception as e:
            RawRecord.objects.create(
                data_source=data_source,
                raw_payload={},
                ingestion_status=RawRecord.Status.FAILED,
                error_message=f"CSV Parsing Error: {str(e)}"
            )
            return {"status": "error", "message": "Invalid CSV format"}

        records_created = 0
        with transaction.atomic():
            for index, row in df.iterrows():
                raw_payload = row.to_dict()
                
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
        Fields: Meter ID, Billing Start, Billing End, kWh, Tariff
        """
        meter_id = payload.get('Meter ID', 'UNKNOWN_METER')
        start_str = payload.get('Billing Start')
        end_str = payload.get('Billing End')
        kwh_raw = payload.get('kWh')
        tariff = payload.get('Tariff', 'standard')

        try:
            # Assuming YYYY-MM-DD
            start_date = datetime.strptime(str(start_str), "%Y-%m-%d").date()
            end_date = datetime.strptime(str(end_str), "%Y-%m-%d").date()
        except (ValueError, TypeError):
             raise ValueError(f"Invalid date format. Expected YYYY-MM-DD")

        try:
            quantity = Decimal(str(kwh_raw))
        except:
            raise ValueError(f"Invalid quantity: {kwh_raw}")

        suspicious_reasons = []
        if quantity < 0:
            suspicious_reasons.append("Negative electricity consumption.")
        if start_date > end_date:
            suspicious_reasons.append("Billing start is after billing end.")
        
        # Grid emission factor (Mock constant: 0.4 kg CO2e / kWh)
        emission_factor = Decimal('0.4')
        estimated_emissions = quantity * emission_factor

        NormalizedRecord.objects.create(
            organization=self.organization,
            raw_record=raw_record,
            category="purchased_electricity",
            scope=2,
            activity_date=start_date, # Use start date as activity date
            quantity=quantity,
            normalized_unit='kWh',
            estimated_emissions=estimated_emissions,
            status=NormalizedRecord.RecordStatus.PENDING_REVIEW,
            suspicious_reason=" | ".join(suspicious_reasons) if suspicious_reasons else None,
            source_of_truth=f"UTILITY_METER_{meter_id}"
        )

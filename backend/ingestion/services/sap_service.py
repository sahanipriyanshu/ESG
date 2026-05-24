import pandas as pd
from decimal import Decimal
from datetime import datetime
from django.db import transaction
from records.models import DataSource, RawRecord, NormalizedRecord
from .base import BaseIngestionService

class SAPService(BaseIngestionService):
    @property
    def source_type(self):
        return DataSource.SourceType.SAP

    def process(self, file_obj):
        data_source = self.create_data_source(file_obj=file_obj)
        
        # Reset file pointer if needed
        file_obj.seek(0)
        
        try:
            df = pd.read_csv(file_obj)
        except Exception as e:
            # If the CSV is completely malformed, we can't even read rows.
            # Create a single failed RawRecord.
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
                
                # 1. Store the exact raw record first
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
        German column mappings:
        Buchungsdatum -> activity_date
        Werk -> source_of_truth (Plant code)
        Treibstoffart -> category
        Menge -> quantity
        Einheit -> normalized_unit
        """
        # Extract fields
        date_str = payload.get('Buchungsdatum')
        plant_code = payload.get('Werk', 'UNKNOWN_PLANT')
        fuel_type = payload.get('Treibstoffart', 'unknown')
        quantity_raw = payload.get('Menge')
        unit_raw = payload.get('Einheit', '')

        # Date normalization
        try:
            # Assuming YYYY-MM-DD or DD.MM.YYYY
            if '.' in str(date_str):
                activity_date = datetime.strptime(str(date_str), "%d.%m.%Y").date()
            else:
                activity_date = datetime.strptime(str(date_str), "%Y-%m-%d").date()
        except (ValueError, TypeError):
             raise ValueError(f"Invalid date format: {date_str}")

        # Quantity normalization
        try:
            quantity = Decimal(str(quantity_raw))
        except:
            raise ValueError(f"Invalid quantity: {quantity_raw}")

        # Unit normalization
        unit_raw = str(unit_raw).lower()
        if unit_raw in ['l', 'liter', 'liters']:
            normalized_unit = 'L'
        elif unit_raw in ['gal', 'gallon', 'gallons']:
            # Convert to Liters
            quantity = quantity * Decimal('3.78541')
            normalized_unit = 'L'
        else:
            normalized_unit = str(unit_raw).upper()

        # Suspicious Detection
        suspicious_reasons = []
        status = NormalizedRecord.RecordStatus.PENDING_REVIEW
        
        if quantity < 0:
            suspicious_reasons.append("Negative quantity detected.")
        if quantity > 10000:
            suspicious_reasons.append("Unusually large quantity (>10,000).")
        if activity_date > datetime.now().date():
            suspicious_reasons.append("Activity date is in the future.")
        if normalized_unit not in ['L', 'KG', 'KWH']:
            suspicious_reasons.append(f"Unknown unit: {normalized_unit}.")

        # Emissions Estimation (Mock constants based on fuel type)
        # E.g., Diesel ~ 2.68 kg CO2e / L
        emission_factor = Decimal('2.5') # Generic fallback
        if 'diesel' in fuel_type.lower():
            emission_factor = Decimal('2.68')
        elif 'benzin' in fuel_type.lower(): # petrol
            emission_factor = Decimal('2.31')
            
        estimated_emissions = quantity * emission_factor

        NormalizedRecord.objects.create(
            organization=self.organization,
            raw_record=raw_record,
            category=f"stationary_combustion_{fuel_type.lower()}",
            scope=1,
            activity_date=activity_date,
            quantity=quantity,
            normalized_unit=normalized_unit,
            estimated_emissions=estimated_emissions,
            status=status,
            suspicious_reason=" | ".join(suspicious_reasons) if suspicious_reasons else None,
            source_of_truth=f"SAP_{plant_code}"
        )

import abc
from django.db import transaction
from records.models import DataSource, RawRecord

class BaseIngestionService(abc.ABC):
    def __init__(self, organization, mode='api'):
        self.organization = organization
        self.mode = mode
    
    @property
    @abc.abstractmethod
    def source_type(self):
        pass

    def create_data_source(self, file_obj=None):
        return DataSource.objects.create(
            organization=self.organization,
            source_type=self.source_type,
            ingestion_mode=self.mode,
            original_file=file_obj
        )

    @abc.abstractmethod
    def process(self, payload_or_file):
        """
        Process the payload or file, create RawRecords and NormalizedRecords.
        """
        pass

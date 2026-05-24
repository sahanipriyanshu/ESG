from rest_framework import generics
from .models import AuditLog
from .serializers import AuditLogSerializer

class AuditLogListView(generics.ListAPIView):
    serializer_class = AuditLogSerializer

    def get_queryset(self):
        queryset = AuditLog.objects.all()
        
        # Filter by object_id (record_id)
        record_id = self.request.query_params.get('record_id', None)
        if record_id:
            queryset = queryset.filter(object_id=record_id)
            
        return queryset

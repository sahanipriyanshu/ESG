from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import NormalizedRecord
from .serializers import NormalizedRecordSerializer, RecordActionSerializer
from .services import RecordWorkflowService

class NormalizedRecordListView(generics.ListAPIView):
    serializer_class = NormalizedRecordSerializer

    def get_queryset(self):
        queryset = NormalizedRecord.objects.all()
        # Optional filtering
        suspicious = self.request.query_params.get('suspicious', None)
        record_status = self.request.query_params.get('status', None)
        
        if suspicious == 'true':
            queryset = queryset.exclude(suspicious_reason__isnull=True).exclude(suspicious_reason='')
        elif suspicious == 'false':
            queryset = queryset.filter(suspicious_reason__isnull=True) | queryset.filter(suspicious_reason='')
            
        if record_status:
            queryset = queryset.filter(status=record_status)
            
        return queryset

class RecordApproveView(APIView):
    def post(self, request, pk):
        try:
            record = NormalizedRecord.objects.get(pk=pk)
        except NormalizedRecord.DoesNotExist:
            return Response({"error": "Record not found"}, status=status.HTTP_404_NOT_FOUND)
            
        serializer = RecordActionSerializer(data=request.data)
        if serializer.is_valid():
            try:
                updated_record = RecordWorkflowService.approve_record(
                    record=record,
                    actor=serializer.validated_data['actor']
                )
                return Response(NormalizedRecordSerializer(updated_record).data)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RecordRejectView(APIView):
    def post(self, request, pk):
        try:
            record = NormalizedRecord.objects.get(pk=pk)
        except NormalizedRecord.DoesNotExist:
            return Response({"error": "Record not found"}, status=status.HTTP_404_NOT_FOUND)
            
        serializer = RecordActionSerializer(data=request.data)
        if serializer.is_valid():
            try:
                updated_record = RecordWorkflowService.reject_record(
                    record=record,
                    actor=serializer.validated_data['actor'],
                    reason=serializer.validated_data.get('reason')
                )
                return Response(NormalizedRecordSerializer(updated_record).data)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RecordLockView(APIView):
    def post(self, request, pk):
        try:
            record = NormalizedRecord.objects.get(pk=pk)
        except NormalizedRecord.DoesNotExist:
            return Response({"error": "Record not found"}, status=status.HTTP_404_NOT_FOUND)
            
        serializer = RecordActionSerializer(data=request.data)
        if serializer.is_valid():
            try:
                updated_record = RecordWorkflowService.lock_record(
                    record=record,
                    actor=serializer.validated_data['actor']
                )
                return Response(NormalizedRecordSerializer(updated_record).data)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

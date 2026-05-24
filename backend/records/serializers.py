from rest_framework import serializers
from .models import NormalizedRecord

class NormalizedRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = NormalizedRecord
        fields = '__all__'

class RecordActionSerializer(serializers.Serializer):
    actor = serializers.CharField(max_length=255, default='System Analyst')
    reason = serializers.CharField(max_length=500, required=False, allow_blank=True)

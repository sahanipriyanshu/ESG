from rest_framework import serializers
from organizations.models import Organization

class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    organization_id = serializers.UUIDField()

    def validate_organization_id(self, value):
        if not Organization.objects.filter(id=value).exists():
            raise serializers.ValidationError("Organization not found.")
        return value

class TravelPayloadSerializer(serializers.Serializer):
    organization_id = serializers.UUIDField()
    payloads = serializers.ListField(
        child=serializers.DictField(),
        min_length=1
    )

    def validate_organization_id(self, value):
        if not Organization.objects.filter(id=value).exists():
            raise serializers.ValidationError("Organization not found.")
        return value

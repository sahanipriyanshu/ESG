from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from organizations.models import Organization
from .serializers import FileUploadSerializer, TravelPayloadSerializer
from .services.sap_service import SAPService
from .services.utility_service import UtilityService
from .services.travel_service import TravelService

class SAPIngestionView(APIView):
    def post(self, request):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            org = Organization.objects.get(id=serializer.validated_data['organization_id'])
            file_obj = serializer.validated_data['file']
            
            service = SAPService(organization=org, mode='api')
            result = service.process(file_obj)
            
            if result.get('status') == 'success':
                return Response(result, status=status.HTTP_201_CREATED)
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UtilityIngestionView(APIView):
    def post(self, request):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            org = Organization.objects.get(id=serializer.validated_data['organization_id'])
            file_obj = serializer.validated_data['file']
            
            service = UtilityService(organization=org, mode='api')
            result = service.process(file_obj)
            
            if result.get('status') == 'success':
                return Response(result, status=status.HTTP_201_CREATED)
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TravelIngestionView(APIView):
    def post(self, request):
        serializer = TravelPayloadSerializer(data=request.data)
        if serializer.is_valid():
            org = Organization.objects.get(id=serializer.validated_data['organization_id'])
            payloads = serializer.validated_data['payloads']
            
            service = TravelService(organization=org, mode='api')
            result = service.process(payloads)
            
            if result.get('status') == 'success':
                return Response(result, status=status.HTTP_201_CREATED)
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

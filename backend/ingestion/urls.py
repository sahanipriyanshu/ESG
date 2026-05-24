from django.urls import path
from .views import SAPIngestionView, UtilityIngestionView, TravelIngestionView

urlpatterns = [
    path('sap/', SAPIngestionView.as_view(), name='sap-ingestion'),
    path('utility/', UtilityIngestionView.as_view(), name='utility-ingestion'),
    path('travel/', TravelIngestionView.as_view(), name='travel-ingestion'),
]

from django.urls import path
from .views import NormalizedRecordListView, RecordApproveView, RecordRejectView, RecordLockView

urlpatterns = [
    path('', NormalizedRecordListView.as_view(), name='record-list'),
    path('<uuid:pk>/approve/', RecordApproveView.as_view(), name='record-approve'),
    path('<uuid:pk>/reject/', RecordRejectView.as_view(), name='record-reject'),
    path('<uuid:pk>/lock/', RecordLockView.as_view(), name='record-lock'),
]

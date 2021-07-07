from django.urls import path
from .views import (
    OverviewAPIView,
    AccountingAPIView
)

urlpatterns = [
    path('overview/', OverviewAPIView.as_view(),name='overview'),
    path('accounting/', AccountingAPIView.as_view(),name='accounting'),
]
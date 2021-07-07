from django.urls import path
from .views.overview import (
    DashboardAPIView,
)

urlpatterns = [
    path('', DashboardAPIView.as_view(),name='dashboard'),
]
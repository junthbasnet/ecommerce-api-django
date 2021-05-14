from django.urls import path, include

from .routers import router
from .views import MarkAllAsReadAPI

urlpatterns = [
    path('', include(router.urls)),
    path('mark-all-as-read/', MarkAllAsReadAPI.as_view(), name='mark_all_as_read'),
]

from django.urls import path, include

from .routers import router
from .views import (
    RegisterUserAPIView,
    ObtainAuthTokenView,
    FacebookDataDeletion,
    CheckUserDeletionStatus,
)

app_name = 'users'

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterUserAPIView.as_view(), name='register'),
    path('login/', ObtainAuthTokenView.as_view()),
    path('facebook-data-delete/', FacebookDataDeletion.as_view()),
    path('check-status/', CheckUserDeletionStatus.as_view()),
]

from rest_framework.routers import DefaultRouter

from .views import (
    UserAPIViewSet,
    UserProfileAPIViewSet,
)

router = DefaultRouter()
router.register('profile', UserProfileAPIViewSet, basename='profile')
router.register('user-list', UserAPIViewSet, basename='users_list')

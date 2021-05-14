from rest_framework.routers import DefaultRouter

from .views import NotificationAPI

router = DefaultRouter()
router.register('notification-list', NotificationAPI)

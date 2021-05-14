from django.contrib.auth import get_user_model

from .models import Notification

users = get_user_model().objects.filter(is_staff=True)


def bulk_create_notification_admin(data):
    for user in users:
        Notification.objects.create(**data, user=user)

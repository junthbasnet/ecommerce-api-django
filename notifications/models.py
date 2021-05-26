from django.db import models

from common.models import TimeStampedModel


class Notification(TimeStampedModel):
    title = models.CharField(max_length=100)
    body = models.TextField()
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.title}'

from django.db import models
from django.utils.text import slugify

from common.models import TimeStampedModel


class Newsletter(TimeStampedModel):
    title = models.CharField(max_length=225, unique=True)
    slug = models.SlugField(default="", max_length=255)
    email_subject = models.CharField(max_length=500)
    content = models.TextField()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Newsletter, self).save(*args, **kwargs)


class Subscriber(models.Model):
    email = models.EmailField(default='admin@admin.com', unique=True)
    code = models.CharField(max_length=500, default='', blank=True)

    def __str__(self):
        return self.email

# Register your models here.
from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from newsletter.tasks import send_subscription_email
from .models import Newsletter, Subscriber
from .serializers import NewsletterSerializer, SubscriberSerializer


class SendMailMixin:
    def send_mail(self, request, queryset):
        subscribers = Subscriber.objects.all()
        subscribers = SubscriberSerializer(subscribers, many=True).data
        for newsletter in queryset:
            newsletter = NewsletterSerializer(newsletter).data
            send_subscription_email.delay(subscribers, newsletter)

    send_mail.short_description = "Send Selected Newsletter to all subscribers"


class NewsletterAdmin(SummernoteModelAdmin, SendMailMixin):
    summernote_fields = ('content',)
    actions = ['send_mail']
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Newsletter, NewsletterAdmin)
admin.site.register(Subscriber)

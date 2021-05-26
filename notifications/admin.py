from django.contrib import admin

from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'created_on',)
    list_filter = ('user__is_staff',)
    search_fields = ('title', 'body', 'user__email',)
    fieldsets = (
        (
            'General', {
            'fields': (
                'title','body', 'user', 'is_read',
            )
        }),
        (
            'Important Dates', {
            'fields': (
                'created_on', 'modified_on',
            ),
        }),
    )

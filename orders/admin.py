from django.contrib import admin

from .models import (
    PromoCode
)

@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'discount', 'start_date', 'end_date',)
    search_fields = ('name', 'code', )
    fieldsets = (
        (
            'General', {
            'fields': (
                'name', 'code', 'discount', 'start_date', 'end_date',
            )
        }),
        (
            'Important Dates', {
            'fields': (
                'created_on', 'modified_on',
            ),
        }),
    )

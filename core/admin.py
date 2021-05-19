from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import (
    SiteSetting,
    SEOSetting,
    SocialLinkSetting,
    Slideshow,
    FAQCategory,
    FAQ,
    PaymentMethod,
    Testimonial,
    Province,
    City,
    Area,
)


@admin.register(SiteSetting)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('site_title', 'contact_number', 'address', 'email')


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'info', 'description', )


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('id' ,'method_name', 'charge', 'icon_thumbnail', 'priority')
    list_filter = ('priority',)
    search_fields = ('method_name',)
    prepopulated_fields = {'slug': ('method_name',)}

    fieldsets = (
        (
            'General', {
            'fields': (
                'method_name', 'slug', 'charge', 'icon', 'priority',
            )
        }),
        (
            'Important Dates', {
            'fields': (
                'created_on', 'modified_on',
            ),
        }),
    )

    def icon_thumbnail(self, obj):
        try:
            img_url=obj.icon.url
        except :
            img_url="https://imgur.com/2pO6gCt.png"
        return mark_safe(f'<img src="{img_url}" style="width:15vh;object-fit:cover;"/>')


@admin.register(SEOSetting)
class SEOSettingsAdmin(admin.ModelAdmin):
    list_display = ('og_title',)


@admin.register(SocialLinkSetting)
class SocialLinkSettingAdmin(admin.ModelAdmin):
    list_display = ('platform', 'link', 'icon',)



@admin.register(FAQCategory)
class FAQCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('category', 'question', 'answer', 'slug', 'is_active')
    list_filter = ('category', 'is_active')
    prepopulated_fields = {'slug': ('question',)}
    exclude = ['modified_on', 'created_on', ]


@admin.register(Slideshow)
class SlideshowAdmin(admin.ModelAdmin):
    list_display = ('link', 'caption', 'is_active',)
    exclude = ['modified_on', 'created_on', ]
    list_filter = ('is_active',)


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name',)
    fieldsets = (
        (
            'General', {
            'fields': (
                'name',
            )
        }),
        (
            'Important Dates', {
            'fields': (
                'created_on', 'modified_on',
            ),
        }),
    )


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'province')
    list_filter = ('province',)
    search_fields = ('name',)
    fieldsets = (
        (
            'General', {
            'fields': (
                'name', 'province',
            )
        }),
        (
            'Important Dates', {
            'fields': (
                'created_on', 'modified_on',
            ),
        }),
    )


@admin.register(Area)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'city', 'delivery_duration',)
    list_filter = ('city',)
    search_fields = ('name',)
    fieldsets = (
        (
            'General', {
            'fields': (
                'name', 'city', 'delivery_duration',
            )
        }),
        (
            'Important Dates', {
            'fields': (
                'created_on', 'modified_on',
            ),
        }),
    )

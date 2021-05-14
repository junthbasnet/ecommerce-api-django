from django.contrib import admin

from .models import (
    SiteSetting,
    SEOSetting,
    SocialLinkSetting,
    Slideshow,
    FAQCategory,
    FAQ,
    PaymentMethod,
    Testimonial,
)


@admin.register(SiteSetting)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('site_title', 'contact_number', 'address', 'email')


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'info', 'description', )


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('id' ,'method_name', 'charge')


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

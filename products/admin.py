from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import (
    Category,
    SubCategory,
    Product,
    GlobalSpecification,
    ProductColor,
    ProductImage,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'priority', 'image_thumbnail',)
    list_filter = ('priority',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        (
            'General', {
            'fields': (
                'name','slug', 'description', 'image', 'priority',
            )
        }),

        (
            'SEO', {
            'fields': (
                'og_url', 'og_title', 'og_description', 'og_image', 'meta_title', 'meta_description', 'keywords', 'tags',
            ),
        }),
        (
            'Important Dates', {
            'fields': (
                'created_on', 'modified_on',
            ),
        }),
    )

    def image_thumbnail(self, obj):
        try:
            img_url=obj.image.url
        except :
            img_url="https://imgur.com/2pO6gCt.png"
        return mark_safe(f'<img src="{img_url}" style="height:15vh; width:15vh;object-fit:cover;"/>')
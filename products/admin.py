from django.contrib import admin
from django.utils.safestring import mark_safe
from django.db import models
from django_json_widget.widgets import JSONEditorWidget
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
        return mark_safe(f'<img src="{img_url}" style="width:15vh;object-fit:cover;"/>')


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'image_thumbnail',)
    list_filter = ('category',)
    search_fields = ('name', 'description', 'category__name', 'category__description',)
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        (
            'General', {
            'fields': (
                'category', 'name', 'slug', 'description', 'image',
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
        return mark_safe(f'<img src="{img_url}" style="width:15vh;object-fit:cover;"/>')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'sub_category', 'brand', 'quantity', 'selling_price','image_thumbnail',)
    list_filter = ('sub_category', 'sub_category__category', 'brand',)
    search_fields = ('name', 'overview', 'sub_category__name', 'sub_category__description',)
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        (
            'General', {
            'fields': (
                'sub_category', 'name', 'slug', 'brand', 'image',
                'quantity', 'items_sold', 'marked_price', 'selling_price', 'overview',
            )
        }),
        (
            'Specification', {
            'fields': (
                'specifications',
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
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }

    def image_thumbnail(self, obj):
        try:
            img_url=obj.image.url
        except :
            img_url="https://imgur.com/2pO6gCt.png"
        return mark_safe(f'<img src="{img_url}" style="width:15vh;object-fit:cover;"/>')


@admin.register(GlobalSpecification)
class GlobalSpecificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        (
            'General', {
            'fields': (
                'name', 'slug',
            )
        }),
        (
            'Important Dates', {
            'fields': (
                'created_on', 'modified_on',
            ),
        }),
    )


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'color', 'image_thumbnail',)
    list_filter = ('color', 'color__product',)
    fieldsets = (
        (
            'General', {
            'fields': (
                'color', 'image',
            )
        }),
    )

    def image_thumbnail(self, obj):
        try:
            img_url=obj.image.url
        except :
            img_url="https://imgur.com/2pO6gCt.png"
        return mark_safe(f'<img src="{img_url}" style="width:15vh;object-fit:cover;"/>')


class ProductImageInline(admin.TabularInline):
    model =  ProductImage
    extra = 1


@admin.register(ProductColor)
class ProductColorAdmin(admin.ModelAdmin):
    list_display = ('id', 'product','name', 'code',)
    list_filter = ('product',)
    search_fields = ('name', 'code', 'product__name',)
    fieldsets = (
        (
            'General', {
            'fields': (
                'product', 'name', 'code',
            )
        }),
        (
            'Important Dates', {
            'fields': (
                'created_on', 'modified_on',
            ),
        }),
    )
    inlines = [
        ProductImageInline,
    ]



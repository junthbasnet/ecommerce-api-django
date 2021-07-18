from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import (
    PromoCode,
    Order,
    OrderProduct,
    PreOrderProductBundle,
)
from products.models import RatingAndReview

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


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'payment', 'delivery_status','estimated_delivery_date',
        'delivered_at', 'shipping', 'order_uuid', 'discount',
        'delivery_charge', 'vat', 'sub_total', 'final_price',
    )
    list_filter = ('delivery_status', 'payment__method')
    search_fields = ('user__email', 'order_uuid', 'payment__payment_uuid',)
    fieldsets = (
        (
            'General', {
            'fields': (
                'user', 'payment', 'delivery_status', 'estimated_delivery_date',
                'delivered_at', 'shipping', 'order_uuid', 'discount', 'delivery_charge',
                'vat', 'sub_total', 'final_price',
            )
        }),
        (
            'Important Dates', {
            'fields': (
                'created_on', 'modified_on', 'deleted_on', 'is_deleted'
            ),
        }),
    )



@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'order', 'user', 'product', 'color', 'quantity', 'rate',
        'net_total', 'delivery_status', 'estimated_delivery_date',
        'delivered_at', 'to_be_reviewed', 'image_thumbnail',
    )
    list_filter = ('delivery_status','to_be_reviewed',)
    search_fields = (
        'user__email', 'order__order_uuid',
        'order__payment__payment_uuid',
    )
    fieldsets = (
        (
            'General', {
            'fields': (
                'user', 'product', 'order', 'color', 'quantity', 'rate',
                'net_total', 'delivery_status', 'estimated_delivery_date',
                'delivered_at',
            )
        }),
        (
            'Review', {
            'fields': (
                'to_be_reviewed', 'reviews',
            )
        }),
        (
            'Important Dates', {
            'fields': (
                'created_on', 'modified_on', 'deleted_on', 'is_deleted'
            ),
        }),
    )

    def image_thumbnail(self, obj):
        try:
            img_url=obj.product.hero_image.url
        except :
            img_url="https://imgur.com/2pO6gCt.png"
        return mark_safe(f'<img src="{img_url}" style="width:15vh;object-fit:cover;"/>')



@admin.register(PreOrderProductBundle)
class PreOrderProductBundleAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'payment', 'product_bundle', 'quantity', 'rate', 'delivery_status', 'delivered_at', 'shipping', 'pre_order_uuid', 'final_price'
    )
    list_filter = ('delivery_status', 'payment__method')
    search_fields = ('user__email', 'pre_order_uuid', 'payment__payment_uuid',)
    fieldsets = (
        (
            'General', {
            'fields': (
                'user', 'payment','product_bundle', 'quantity', 'rate', 'delivery_status', 'estimated_delivery_date','delivered_at', 'shipping',
                'pre_order_uuid', 'discount', 'delivery_charge', 'final_price'
            )
        }),
        (
            'Important Dates', {
            'fields': (
                'created_on', 'modified_on', 'deleted_on', 'is_deleted'
            ),
        }),
    )

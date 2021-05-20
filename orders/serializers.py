from rest_framework import serializers
from .models import (
    PromoCode,
    Order,
    OrderProduct
)
from .utils import (
    validate_payment,
    validate_final_price_client_server,
    validate_final_price_with_payment_obj,
    is_quantity_less_than_or_equal_to,
)
from users.serializers import (
    UserSerializer,
    ShippingSerializer,
)
from products.serializers import (
    ProductSerializer,
)


class PromoCodeSerializer(serializers.ModelSerializer):
    """
    Serializes Promocode model instances.
    """
    class Meta:
        model = PromoCode
        fields='__all__'
        read_only_fields = ('created_on', 'modified_on')


class OrderProductSerializer(serializers.ModelSerializer):
    """
    Serializes OrderProduct model instances.
    """
    product = ProductSerializer(read_only=True)
    class Meta:
        model = OrderProduct
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializes Order model instances.
    """
    payment_uuid = serializers.CharField(max_length=63, write_only=True, required=True)
    cart_items = serializers.ListField(allow_empty=False, write_only=True)
    products = OrderProductSerializer(many=True, read_only=True)
    user = serializers.SerializerMethodField()
    shipping_data = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = (
            'id', 'order_uuid', 'user', 'payment', 'delivery_status', 'estimated_delivery_date',
            'delivered_at', 'shipping', 'discount', 'delivery_charge', 'final_price', 'cart_items',
            'payment_uuid', 'products', 'shipping_data', 'created_on', 'modified_on',
        )
        read_only_fields = (
            'order_uuid', 'user', 'payment', 'delivery_status', 'estimated_delivery_date',
            'delivered_at',
        )
    
    def get_user(self, obj):
        return UserSerializer(self.context['request'].user).data

    def get_shipping_data(self, obj):
        return ShippingSerializer(obj.shipping).data
    
    def validate(self, data):
        """
        Check payment.
        """
        user = self.context['request'].user
        payment_uuid = data.get('payment_uuid', None)
        client_final_price = data.get('final_price', None)
        delivery_charge = data.get('delivery_charge', 0)
        discount = data.get('discount', 0)
        cart_items = data.get('cart_items')
        shipping = data.get('shipping', None)
        if not shipping:
            raise serializers.ValidationError(
                {
                    'error_message': [
                        f"shipping id is needed."
                    ]
                },
                code='no_shipping'
            )

        payment_obj = validate_payment(payment_uuid, user)
        payment_obj.order_assigned=True
        payment_obj.save()

        is_quantity_less_than_or_equal_to(cart_items)
        validate_final_price_client_server(client_final_price, delivery_charge, discount, cart_items)
        validate_final_price_with_payment_obj(payment_obj, delivery_charge, discount, cart_items)

        data['final_price'] = payment_obj.amount
        data['payment_obj'] = payment_obj
        return data
    




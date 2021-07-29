from rest_framework import serializers
from .models import (
    PromoCode,
    Order,
    OrderProduct,
    PreOrderProductBundle,
)
from .utils import (
    validate_payment,
    validate_final_price_client_server,
    validate_final_price_with_payment_obj,
    is_quantity_less_than_or_equal_to,
    validate_final_price_client_server_for_pre_order,
    validate_final_price_of_pre_order_with_payment_obj,
    validate_vat_calculation,
    validate_vat_calculation_for_preorder,
)
from users.serializers import (
    UserSerializer,
    ShippingSerializer,
)
from products.serializers import (
    ProductSerializer,
    RatingAndReviewSerializer,
    ProductBundleForPreOrderSerializer,
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
    reviews = RatingAndReviewSerializer(read_only=True)
    class Meta:
        model = OrderProduct
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializes Order model instances.
    """
    payment_uuid = serializers.CharField(max_length=63, write_only=True, required=True)
    payment_name = serializers.CharField(source='payment.method.method_name', read_only=True)
    cart_items = serializers.ListField(allow_empty=False, write_only=True)
    vat = serializers.DecimalField(max_digits=10, decimal_places=2)
    products_price = serializers.DecimalField(max_digits=10, decimal_places=2, write_only=True)
    products = OrderProductSerializer(many=True, read_only=True)
    user = serializers.SerializerMethodField(read_only=True)
    shipping_data = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = (
            'id', 'order_uuid', 'user', 'payment', 'delivery_status', 'estimated_delivery_date',
            'delivered_at', 'shipping', 'discount', 'delivery_charge', 'final_price', 'cart_items',
            'payment_uuid', 'products', 'shipping_data', 'created_on', 'modified_on', 'vat',
            'products_price', 'payment_name', 'sub_total', 'reward_points',
        )
        read_only_fields = (
            'order_uuid', 'user', 'payment', 'delivery_status', 'estimated_delivery_date',
            'delivered_at', 'reward_points',
        )
    
    def get_user(self, obj):
        return UserSerializer(self.context['request'].user).data

    def get_shipping_data(self, obj):
        return ShippingSerializer(obj.shipping).data
    
    def validate(self, data):
        """
        Check payment, quantity, price.
        """
        user = self.context['request'].user
        payment_uuid = data.get('payment_uuid', None)
        client_final_price = data.get('final_price', None)
        delivery_charge = data.get('delivery_charge', 0)
        discount = data.get('discount', 0)
        vat = data.get('vat', None)
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
        

        validate_vat_calculation(vat, cart_items)
        validate_final_price_client_server(client_final_price, delivery_charge, discount, cart_items, vat)
        is_quantity_less_than_or_equal_to(cart_items)
        payment_obj = validate_payment(payment_uuid, user)
        validate_final_price_with_payment_obj(payment_obj, delivery_charge, discount, cart_items, vat)
        payment_obj.order_assigned=True
        payment_obj.save()

        data['final_price'] = payment_obj.amount
        data['payment_obj'] = payment_obj
        return data
    

class PreOrderProductBundleSerializer(serializers.ModelSerializer):
    """
    Serializes PreOrderProductBundle model instances.
    """
    payment_uuid = serializers.CharField(max_length=63, write_only=True, required=True)
    product_bundle_data = serializers.SerializerMethodField(read_only=True)
    vat = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model=PreOrderProductBundle
        fields = (
            'id', 'pre_order_uuid', 'product_bundle', 'quantity', 'user', 'payment',
            'delivery_status', 'estimated_delivery_date', 'delivered_at', 'shipping',
            'discount', 'delivery_charge', 'final_price', 'payment_uuid',
            'created_on', 'modified_on', 'product_bundle_data', 'vat',
        )
        read_only_fields = (
            'pre_order_uuid', 'user', 'payment', 'delivery_status',
            'estimated_delivery_date', 'delivered_at',
        )
    
    def get_product_bundle_data(self, obj):
        return ProductBundleForPreOrderSerializer(
            obj.product_bundle, 
            context={'request':self.context['request']}
        ).data

    def validate(self, data):
        """
        Check payment, price.
        """
        user = self.context['request'].user
        product_bundle_obj = data.get('product_bundle', None)
        payment_uuid = data.get('payment_uuid', None)
        client_final_price = data.get('final_price', None)
        delivery_charge = data.get('delivery_charge', 0)
        vat = data.get('vat', 0)
        quantity = data.get('quantity', 1)
        discount = data.get('discount', 0)
        shipping = data.get('shipping', None)

        # Required : shipping and product_bundle (ID)
        if not shipping:
            raise serializers.ValidationError(
                {
                    'error_message': [
                        f"shipping id is needed."
                    ]
                },
                code='no_shipping'
            )
        if not product_bundle_obj:
            raise serializers.ValidationError(
                {
                    'error_message': [
                        f"product_bundle id is needed."
                    ]
                },
                code='no_product_bundle'
            )
        validate_vat_calculation_for_preorder(vat, product_bundle_obj.selling_price * quantity)
        validate_final_price_client_server_for_pre_order(
            client_final_price, 
            delivery_charge, 
            discount, 
            product_bundle_obj,
            quantity,
            vat,
        )
        payment_obj = validate_payment(payment_uuid, user)
        validate_final_price_of_pre_order_with_payment_obj(
            payment_obj, 
            delivery_charge, 
            discount, 
            product_bundle_obj, 
            quantity,
            vat
        )
        payment_obj.order_assigned=True
        payment_obj.save()


        data['final_price'] = payment_obj.amount
        data['payment_obj'] = payment_obj
        return data


class OrderCheckoutCalculationSerializer(serializers.Serializer):
    """
    Validates whether following fields are set during checkout.
    """
    cart_items = serializers.ListField(
        child=serializers.DictField(allow_empty=False),
        allow_empty=False
    )
    shipping = serializers.IntegerField(required=True)
    promocode = serializers.CharField(max_length=64, required=False)


class PreOrderCheckoutCalculationSerializer(serializers.Serializer):
    """
    Validates whether following fields are set during pre-order checkout.
    """
    shipping = serializers.IntegerField(required=True)
    product_bundle = serializers.IntegerField(required=True)
    quantity = serializers.IntegerField(required=True)
    promocode = serializers.CharField(max_length=64, required=False)
    
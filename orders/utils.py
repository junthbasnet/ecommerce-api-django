from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from rest_framework import serializers
from payments.models import Payment
from products.models import Product
from .models import Order, OrderProduct, PreOrderProductBundle


def validate_payment(payment_uuid, user):
    """
    1. Check if payment object with that payment_uuid exists.
    2. Check if order is already assigned with that payment_uuid.

    Raises validation error or returns payment_obj.
    """
    try:
        payment_obj = Payment.objects.get(
            payment_uuid=payment_uuid,
            order_assigned=False,
            user=user,
        )
    except ObjectDoesNotExist or MultipleObjectsReturned:
        raise serializers.ValidationError(
            {
                'error_message': [
                    "Payment object with given payment doesnt exist or order is already assigned with this payment_uuid."
                ]
            },
            code='invalid_payment_uuid'
        )
    return payment_obj


def get_product_obj(product_id):
    """
    Raises validation error or returns product_obj.
    """
    try:
        product_obj = Product.objects.get(pk=product_id)
    except ObjectDoesNotExist or MultipleObjectsReturned:
        raise serializers.ValidationError(
            {
                'error_message': [
                    f"Product with product_id:{product_id} doesn't exist."
                ]
            },
            code='invalid_product_id'
        )
    return product_obj


def calculate_final_price(delivery_charge, discount, cart_items):
    """
    Calculates final price from cart items.
    """
    product_price_list = []
    for cart_item in cart_items:
        product_id = cart_item.get('product_id', None)
        product_quantity = cart_item.get('quantity', None)
        product_obj = get_product_obj(product_id)
        per_product_price = product_obj.selling_price
        product_price = per_product_price * product_quantity
        product_price_list.append(product_price)
    products_price =  sum(product_price_list)
    calculated_final_price = products_price + delivery_charge - discount
    return calculated_final_price


def validate_final_price_client_server(client_final_price, delivery_charge, discount, cart_items):
    """
    Returns True or raises validation error.
    """
    calculated_final_price = calculate_final_price(delivery_charge, discount, cart_items)
    if calculated_final_price != client_final_price:
        raise serializers.ValidationError(
            {
                'error_message': [
                    f"Client final price: {client_final_price}. Server final price: {calculated_final_price}"
                ]
            },
            code='invalid_final_price'
        )
    return True


def validate_final_price_with_payment_obj(payment_obj, delivery_charge, discount, cart_items):
    """
    Returns True or raises validation error.
    """
    calculated_final_price = calculate_final_price(delivery_charge, discount, cart_items)
    if payment_obj.amount < calculated_final_price:
        raise serializers.ValidationError(
            {
                'error_message': [
                    f"You ordered products worth {calculated_final_price}  but paid {payment_obj.amount}"
                ]
            },
            code='insufficient_payment'
        )
    return True


def check_product_quantity(product_obj, product_quantity):
    """
    Returns True if product_quantity is less than or equal to product_obj quantity.
    """
    if product_quantity <= product_obj.quantity:
        return True
    raise serializers.ValidationError(
        {
            'error_message': [
                f"You ordered {product_quantity} {product_obj.name}, but the stock has only {product_obj.quantity}"
            ]
        },
        code='insufficient_quantity'
    )
    

def is_quantity_less_than_or_equal_to(cart_items):
    """
    Returns True if ordered quantity is less than or equal to the stock quantity.
    """
    for cart_item in cart_items:
        product_id = cart_item.get('product_id', None)
        product_quantity = cart_item.get('quantity', None)
        product_obj = get_product_obj(product_id)
        check_product_quantity(product_obj, product_quantity)
    return True


def get_order_obj(order_id):
    """
    Raises validation error or returns order_obj.
    """
    try:
        order_obj = Order.objects.get(pk=order_id)
    except ObjectDoesNotExist or MultipleObjectsReturned:
        raise serializers.ValidationError(
            {
                'error_message': [
                    f"Order with order_id:{order_id} doesn't exist."
                ]
            },
            code='invalid_order_id'
        )
    return order_obj


def validate_final_price_client_server_for_pre_order(client_final_price, delivery_charge, discount, product_bundle_obj, quantity):
    """
    Returns true or raises validation error.
    """
    calculated_final_price = (product_bundle_obj.selling_price * quantity) - discount + delivery_charge
    if calculated_final_price != client_final_price:
        raise serializers.ValidationError(
            {
                'error_message': [
                    f"Client final price: {client_final_price}. Server final price: {calculated_final_price}"
                ]
            },
            code='invalid_final_price'
        )
    return True


def validate_final_price_of_pre_order_with_payment_obj(payment_obj, delivery_charge, discount, product_bundle_obj, quantity):
    """
    Returns True or raises validation error.
    """
    calculated_final_price = (product_bundle_obj.selling_price * quantity) - discount + delivery_charge
    if payment_obj.amount < calculated_final_price:
        raise serializers.ValidationError(
            {
                'error_message': [
                    f"You ordered products worth {calculated_final_price}  but paid {payment_obj.amount}"
                ]
            },
            code='insufficient_payment'
        )
    return True


def get_pre_order_obj(pre_order_id):
    """
    Raises validation error or returns pre_order_obj.
    """
    try:
        pre_order_obj = PreOrderProductBundle.objects.get(pk=pre_order_id)
    except ObjectDoesNotExist or MultipleObjectsReturned:
        raise serializers.ValidationError(
            {
                'error_message': [
                    f"PreOrderProductBundle with pre_order_id:{pre_order_id} doesn't exist."
                ]
            },
            code='invalid_pre_order_id'
        )
    return pre_order_obj





from notifications.models import Notification
from users.models import User


def notify_user_about_order_creation(order_obj):
    """
    Creates notification object for user about order creation.
    """
    title = f'{order_obj.order_uuid}: Order Placed'
    body = f'Your order has been placed and estimated delivery date is {order_obj.estimated_delivery_date}'
    user = order_obj.user
    Notification.objects.create(
        title=title,
        body=body,
        user=user
    )


def notify_admin_about_order_creation(order_obj):
    """
    Creates notification object for admin about order creation.
    """
    title = f'{order_obj.order_uuid}: Order Placed'
    body = f'Order has been placed by {order_obj.user.email} and estimated delivery date is {order_obj.estimated_delivery_date}'
    for admin in User.objects.filter(is_staff=True):
        Notification.objects.create(
            title=title,
            body=body,
            user=admin
        )


def notify_user_about_pre_order_creation(pre_order_obj):
    """
    Creates notification object for user about pre-order creation.
    """
    title = f'{pre_order_obj.pre_order_uuid}: Pre-Order placed'
    body = f'Your pre-order has been placed.'
    user = pre_order_obj.user
    Notification.objects.create(
        title=title,
        body=body,
        user=user
    )

def notify_admin_about_pre_order_creation(pre_order_obj):
    """
    Creates notification object for admin about pre-order creation.
    """
    title = f'{pre_order_obj.pre_order_uuid}: Pre-order placed'
    body = f'Pre-order has been placed.'
    user = pre_order_obj.user
    for admin in User.objects.filter(is_staff=True):
        Notification.objects.create(
            title=title,
            body=body,
            user=user
        )
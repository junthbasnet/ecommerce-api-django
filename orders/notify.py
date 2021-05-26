from django.template.loader import render_to_string

from common.tasks import send_email
from notifications.models import Notification
from users.models import User


def notify_user_about_order_creation(order_obj):
    """
    Creates notification object for user about order creation.
    """
    title = f'{order_obj.order_uuid}: Order created'
    body = f'Your order has been created and estimated delivery date is {order_obj.estimated_delivery_date}'
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
    title = f'{order_obj.order_uuid}: Order created'
    body = f'Order has been created by {order_obj.user.email} and estimated delivery date is {order_obj.estimated_delivery_date}'
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
    title = f'{pre_order_obj.pre_order_uuid}: Pre-Order created'
    body = f'Your pre-order has been created.'
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
    title = f'{pre_order_obj.pre_order_uuid}: Pre-order created'
    body = f'Pre-order has been created.'
    user = pre_order_obj.user
    for admin in User.objects.filter(is_staff=True):
        Notification.objects.create(
            title=title,
            body=body,
            user=user
        )


def send_order_create_mail_to_user(order_obj):
    """
    Send mail to user after checkout.
    """
    subject = f'Your order has been created successfully.'
    message = f'order ID: {order_obj.order_uuid}'
    context = {
        'order_obj':order_obj
    }
    html_content = render_to_string('order_created.html', context)
    to_mail = [order_obj.user.email, ]
    send_email(
        subject,
        message,
        html_content,
        to_mail,
        from_mail=""
    )


def send_pre_order_create_mail_to_user(pre_order_obj):
    """
    Send mail to user after checkout.
    """
    subject = f'Your order has been created successfully.'
    message = f'order ID: {pre_order_obj.pre_order_uuid}'
    context = {
        'pre_order_obj':pre_order_obj
    }
    html_content = render_to_string('pre_order_created.html', context)
    to_mail = [pre_order_obj.user.email, ]
    send_email(
        subject,
        message,
        html_content,
        to_mail,
        from_mail=""
    )
import pytz
from datetime import timedelta
from django.utils import timezone
from django.db.models.functions import (
    TruncMonth, ExtractMonth, TruncDay,
    TruncDate, Trunc, ExtractDay, TruncWeek,
    ExtractWeek, ExtractWeekDay,
)
from django.db.models import F, Sum, Count
from products.models import Product, Category
from orders.models import Order, OrderProduct


def get_total_orders_from_to(start_date, end_date):
    """
    Returns total orders from start date to end date
    """
    total_orders = (
        OrderProduct.objects
        .filter(created_on__date__range=(start_date, end_date))
        .count()
    )
    return total_orders


def get_orders_pie_chart_category_wise(start_date, end_date):
    """
    Returns list of dict of category_name and count of ordered products under that category.
    """
    category_wise_orders_count = (
        Category.objects
        .filter(sub_categories__products__ordered__created_on__date__range=(start_date, end_date))
        .annotate(order_count=Count('sub_categories__products__ordered'))
        .values('name', 'order_count')
    )
    return category_wise_orders_count


def get_orders_data(start_date, end_date):
    """
    Returns order data from start date to end date.
    """
    orders_data_from_to = (
        OrderProduct.objects.filter(
            created_on__date__range=(start_date, end_date),
        )
        .annotate(date=TruncDate('created_on'),)
        .values('date',)
        .annotate(count=Count('id'))
    )
    return orders_data_from_to


def get_weeks_order_data():
    """
    Returns order data for last 7 days
    """
    start_date = timezone.now().date() - timedelta(days=6)
    end_date = timezone.now().date()
    return get_orders_data(start_date, end_date)
from datetime import timedelta
from django.utils import timezone
from products.models import Product, Category
from orders.models import Order, OrderProduct
from django.db.models import Avg, Max, Min, F, Sum, Count


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
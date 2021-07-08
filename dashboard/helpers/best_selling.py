from datetime import timedelta
from django.utils import timezone
from products.models import Product, Category
from orders.models import Order, OrderProduct
from django.db.models import Avg, Max, Min, F, Sum, Count


def get_best_selling_products(start_date, end_date):
    """
    Returns best selling products with sales count from start date to end date.
    """
    products_with_count = (
        Product.objects
        .filter(ordered__created_on__date__range=(start_date, end_date))
        .annotate(sold_count=Count('ordered'))
        .order_by('-sold_count')
        .values('name', 'sub_category__name', 'sold_count')
    )
    return products_with_count


def get_todays_best_selling_products():
    """
    Returns todays best selling products.
    """
    start_date = timezone.now().date()
    end_date = timezone.now().date()
    return get_best_selling_products(start_date, end_date)


def get_weeks_best_selling_products():
    """
    Returns week best selling products.
    """
    start_date = timezone.now().date() - timedelta(days=6)
    end_date = timezone.now().date()
    return get_best_selling_products(start_date, end_date)
    
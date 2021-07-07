from payments.models import Payment
from datetime import timedelta, date
from django.utils import timezone
from django.db.models.functions import (
    TruncMonth, ExtractMonth, TruncDay,
    TruncDate, Trunc, ExtractDay, TruncWeek,
    ExtractWeek, ExtractWeekDay,
)
from products.models import Product, Category
import pytz
from django.db.models import Avg, Max, Min, F, Sum, Count


def get_sales_data(start_date, end_date):
    """
    Returns weekly sales day wise
    """
    weekly_sales = (
        Payment.objects.filter(
            created_on__date__range=(start_date, end_date),
            payment_status='verified',
            order_assigned=True,
        )
        .annotate(date=TruncDate('created_on'),)
        .values('date',)
        .annotate(sum=Sum('amount'))
    )

    return weekly_sales


def get_total_sales_from_to(start_date, end_date):
    """
    Return total sales amount from start_date to end_date
    """
    total_sales = (
        Payment.objects
        .filter(created_on__date__range=(start_date, end_date))
        .filter(payment_status='verified', order_assigned=True)
        .aggregate(total_sales=Sum('amount'))
        .get('total_sales', 0.00)
    )
    return total_sales


def get_total_sales():
    """
    Returns total sales so far
    """
    total_sales = (
        Payment.objects
        .filter(payment_status='verified', order_assigned=True)
        .aggregate(total_sales=Sum('amount'))
        .get('total_sales', 0.00)
    )
    return total_sales


def get_sales_pie_chart_category_wise(start_date, end_date):
    """
    Returns list of dict of category_name and total sales under that category.
    """
    category_wise_sales = (
        Category.objects
        .filter(sub_categories__products__ordered__created_on__date__range=(start_date, end_date))
        .annotate(sales=Sum('sub_categories__products__ordered__net_total'))
        .values('name', 'sales')
    )
    return category_wise_sales

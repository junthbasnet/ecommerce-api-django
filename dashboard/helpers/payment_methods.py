from datetime import timedelta
from django.utils import timezone
from django.db.models.functions import (
    TruncMonth, ExtractMonth, TruncDay,
    TruncDate, Trunc, ExtractDay, TruncWeek,
    ExtractWeek, ExtractWeekDay,
)
from django.db.models import F, Sum, Count
from products.models import Product, Category
from payments.models import Payment


def get_sales_data_according_to_payment_method_from_to(start_date, end_date):
    """
    Returns sales data according to payment method from given start date
    to end date
    """
    sales_data_from_to = (
        Payment.objects.filter(
            created_on__date__range=(start_date, end_date),
            payment_status='verified',
            order_assigned=True,
        )
        .annotate(payment_method=F('method__method_name'))
        .values('payment_method')
        .annotate(amount=Sum('amount'))
    )
    return sales_data_from_to


def get_weeks_sales_according_to_payment_method():
    """
    Returns sales accoriding to payment method for last 7 days
    """
    start_date = timezone.now().date() - timedelta(days=6)
    end_date = timezone.now().date()
    return get_sales_data_according_to_payment_method_from_to(start_date, end_date)
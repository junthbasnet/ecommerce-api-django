from payments.models import Payment
from datetime import timedelta, date
from django.utils import timezone
from django.db.models.functions import (
    TruncMonth, ExtractMonth, TruncDay,
    TruncDate, Trunc, ExtractDay, TruncWeek,
    ExtractWeek, ExtractWeekDay,
)
import pytz
from django.db.models import Avg, Max, Min, F, Sum


start_date = timezone.now() - timedelta(days=7)
end_date = timezone.now() + timedelta(days=1)


def get_weekly_sales():
    """
    Returns weekly sales
    """
    weekly_sales = (
        Payment.objects.filter(
            created_on__range=(start_date, end_date),
            payment_status='verified',
            order_assigned=True,
        )
        .annotate(date=TruncDate('created_on'),)
        .values('date',)
        .annotate(sum=Sum('amount'))
    )

    return weekly_sales

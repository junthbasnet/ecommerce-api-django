import calendar
from django.db.models import Avg, Max, Min, F, Sum
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models.functions import (
    TruncMonth, ExtractMonth, TruncDay,
    TruncDate, Trunc, ExtractDay, TruncWeek,
    ExtractWeek, ExtractWeekDay,
)
from rest_framework.permissions import (
    IsAdminUser,
)
from payments.models import Payment
from products.models import Product
from orders.models import Order, OrderProduct
from ..helpers.weekly_sales import get_weekly_sales


class DashboardAPIView(APIView):
    """
    APiView that returns weekly, monthly earnings and orders and products meta data.
    """
    permission_classes=(IsAdminUser,)
    def get(self, request, *args, **kwargs):
        # Todays earning
        todays_earnings = (
            Payment.objects.filter(
                payment_status='verified',
                created_on__date=timezone.now().date()
            )
            .aggregate(todays_earnings=Sum('amount'))
            .get('todays_earnings') or 0.00
        )

        # Total earning
        total_earnings = (
            Payment.objects.filter(
                payment_status='verified',
            )
            .aggregate(total_earnings=Sum('amount'))
            .get('total_earnings') or 0.00
        )

        # monthly earnings
        monthly_earnings = (
            Payment.objects.filter(
                payment_status='verified',
            )
            .annotate(
                month=TruncMonth('created_on'),
                month_number=ExtractMonth('created_on')
            )
            .values('month', 'month_number')
            .annotate(sum=Sum('amount'))
        )
        
        formatted_monthly_earnings = []
        for monthly_earning in monthly_earnings:
            monthly_earning['month_name'] = calendar.month_name[monthly_earning['month_number']]
            formatted_monthly_earnings.append(monthly_earning)

        # weekly earnings
        # Truncates to midnight on the Monday of the week.
        weekly_earnings = (
            Payment.objects.filter(
                payment_status='verified',
            )
            .annotate(
                week=TruncWeek('created_on'),
                week_number=ExtractWeek('created_on')
            )
            .values('week', 'week_number')
            .annotate(sum=Sum('amount'))
        )

        # Daily earnings
        daily_earnings = (
            Payment.objects.filter(
                payment_status='verified',
            )
            .annotate(
                day=TruncDay('created_on'),
            )
            .values('day')
            .annotate(sum=Sum('amount'))
        )

        # products and orders metadata.
        products_sold_today = OrderProduct.objects.filter(
                                delivered_at=timezone.now().date(),
                                delivery_status='Completed'
                            ).count()
        orders_received_today = Order.objects.filter(created_on__date=timezone.now().date()).count()
        pending_order = Order.objects.filter(delivery_status='Pending').count()

        weekly_sales = get_weekly_sales()

        return Response(
            {
                # Earnings
                'todays_earnings': todays_earnings,
                # 'total_earnings': total_earnings,
                # 'monthly_earnings': formatted_monthly_earnings,
                # 'weekly_earnings': weekly_earnings,
                # 'daily_earnings': daily_earnings,

                # Products
                'products_sold_today': products_sold_today,

                # Orders
                'orders_received_today': orders_received_today,
                'pending_order': pending_order,

                # weekly sales
                'weekly_sales': weekly_sales
            },
            status.HTTP_200_OK
        )

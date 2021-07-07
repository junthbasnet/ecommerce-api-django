from datetime import timedelta
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from products.models import Product, Category
from orders.models import Order, OrderProduct
from django.contrib.auth import get_user_model
from django.db.models import Avg, Max, Min, F, Sum, Count

from dashboard.helpers.sales import (
    get_total_sales,
    get_sales_data,
    get_total_sales_from_to,
    get_sales_pie_chart_category_wise,
)
from dashboard.helpers.orders import (
    get_total_orders_from_to,
    get_orders_pie_chart_category_wise,
)

User = get_user_model()


class AccountingAPIView(APIView):
    """
    APIView that manages accounting.
    """
    def get(self, request, *args, **kwargs):
        total_sales = get_total_sales()
        products_count = Product.objects.count()
        orders_count = Order.objects.count()
        customers_count = User.objects.filter(is_staff=False, is_superuser=False).count()


        start_date = timezone.now().date() - timedelta(days=6)
        end_date = timezone.now().date()
        weekly_sales = get_sales_data(start_date, end_date)


        orders_today = get_total_orders_from_to(timezone.now().date(), timezone.now().date())
        sales_today = get_total_sales_from_to(timezone.now().date(), timezone.now().date())
        orders_today_pie_chart = get_orders_pie_chart_category_wise(timezone.now().date(), timezone.now().date())
        sales_today_pie_chart = get_sales_pie_chart_category_wise(timezone.now().date(), timezone.now().date())


        return Response(
            {
                # First Row
                'total_sales': total_sales,
                "products": products_count,
                'orders': orders_count,
                'customers': customers_count,

                # Second row
                'weekly_sales': weekly_sales,

                # Third row
                'sales_today': sales_today,
                'orders_today': orders_today,
                'sales_today_pie_chart': sales_today_pie_chart,
                'orders_today_pie_chart': orders_today_pie_chart,
            },
            status.HTTP_200_OK
        )

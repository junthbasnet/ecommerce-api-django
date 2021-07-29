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
    get_weeks_order_data,
)
from dashboard.helpers.best_selling import (
    get_todays_best_selling_products,
    get_weeks_best_selling_products,
)
from dashboard.helpers.payment_methods import (
    get_weeks_sales_according_to_payment_method,
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

        # Piechart - Today
        orders_today = get_total_orders_from_to(timezone.now().date(), timezone.now().date())
        sales_today = get_total_sales_from_to(timezone.now().date(), timezone.now().date()) or 0.00
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

                # Third row : Left
                'sales_today': sales_today,
                'orders_today': orders_today,
                'sales_today_pie_chart': sales_today_pie_chart,
                'orders_today_pie_chart': orders_today_pie_chart,

                # Third Row: Right
                'todays_best_selling_product': get_todays_best_selling_products(),
                'weeks_best_selling_product': get_weeks_best_selling_products(),

                # Fourth  Row
                'order_data_for_last_seven_days': get_weeks_order_data(),
                
                # Fifth Row
                'sales_according_to_payment_method_for_last_seven_days': get_weeks_sales_according_to_payment_method(),
                
            },
            status.HTTP_200_OK
        )

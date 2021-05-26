
from datetime import timedelta
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Avg, Max, Min, F
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import (
    GenericAPIView,
    CreateAPIView,
    ListAPIView, 
    RetrieveAPIView
)
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
)
from rest_framework.views import APIView
from .models import (
    PromoCode,
    Order,
    OrderProduct,
    PreOrderProductBundle,
)
from products.models import (
    Product
)
from .serializers import (
    PromoCodeSerializer,
    OrderSerializer,
    OrderProductSerializer,
    PreOrderProductBundleSerializer,
)
from .utils import (
    get_product_obj,
    get_order_obj,
    get_pre_order_obj,
    generate_order_uuid,
    generate_pre_order_uuid,
    get_estimated_delivery_date,
)
from .notify import (
    notify_user_about_order_creation,
    notify_admin_about_order_creation,
    notify_user_about_pre_order_creation,
    notify_admin_about_pre_order_creation,
    send_order_create_mail_to_user,
    send_pre_order_create_mail_to_user
)


class PromoCodeAPIViewSet(ModelViewSet):
    """
    APIViewSet to manage promo codes.
    """
    serializer_class = PromoCodeSerializer
    queryset = PromoCode.objects.all()


class ApplyPromoCodeGenericAPIView(GenericAPIView):
    """
    APIView to retrieve promocode info during checkout.
    """
    serializer_class = PromoCodeSerializer
    queryset = PromoCode.objects.all()

    def post(self, request, *args, **kwargs):
        promo_code = request.data.get('promo_code', None)
        if promo_code:
            try:
                promo_code_obj = PromoCode.objects.get(code=promo_code)
                if promo_code_obj.is_valid:
                    return Response(self.serializer_class(promo_code_obj).data, status.HTTP_200_OK)
                return Response(
                    {
                        'error_message': 'PromoCode is not valid, you missed your chance.'
                    },
                    status.HTTP_410_GONE
                )
            except ObjectDoesNotExist or MultipleObjectsReturned:
                return Response(
                    {
                        'error_message': f'{promo_code}, Invalid promo-code'
                    },
                    status.HTTP_412_PRECONDITION_FAILED
                )
        return Response(
            {
                'error_message': 'Please provide promocode in request body.'
            },
            status.HTTP_406_NOT_ACCEPTABLE
        )


class CheckOutCreateAPIView(CreateAPIView):
    """
    APIView that manages checkout and creates Order and
    OrderProduct model instances.
    """
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create_order(serializer)
        return Response(
            {
                "message":"successfully ordered."
            },
            status=status.HTTP_201_CREATED
        )

    def perform_create_order(self, serializer):

        payment_obj = serializer.validated_data.get('payment_obj')
        final_price = serializer.validated_data.get('final_price')
        shipping = serializer.validated_data.get('shipping')
        estimated_delivery_date = get_estimated_delivery_date(shipping.area.delivery_duration)

        order_obj = Order.objects.create(
            user = self.request.user,
            payment = payment_obj,
            shipping = shipping,
            discount = serializer.validated_data.get('discount', 0),
            delivery_charge = serializer.validated_data.get('delivery_charge', 0),
            final_price = final_price,
            estimated_delivery_date = estimated_delivery_date
        )
        order_obj.order_uuid = generate_order_uuid(order_obj.pk)
        order_obj.save()
        self.perform_create_order_product(serializer, order_obj)

    def perform_create_order_product(self, serializer, order_obj):
        """
        Create order product object.
        """
        cart_items = serializer.validated_data.get('cart_items')
        for cart_item in cart_items:
            product_id = cart_item.get('product_id', None)
            product_quantity = cart_item.get('quantity', None)
            product_obj = get_product_obj(product_id)
            rate = product_obj.selling_price
            net_total = rate * product_quantity

            color = cart_item.get('color', '')

            OrderProduct.objects.create(
                user = self.request.user,
                product = product_obj,
                order = order_obj,
                color = color,
                quantity = product_quantity,
                rate = rate,
                net_total = net_total,
                estimated_delivery_date = order_obj.estimated_delivery_date  
            )
        send_order_create_mail_to_user(order_obj)
        notify_user_about_order_creation(order_obj)
        notify_admin_about_order_creation(order_obj)
        
    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'request': self.request,
        }


class OrderListAPIView(ListAPIView):
    """
    APIView that lists user orders.
    """
    serializer_class = OrderSerializer
    queryset = Order.objects.none()
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('order_uuid', )
    ordering_fields = ('created_on', 'delivered_at')
    filterset_fields = ('delivery_status', 'user',)

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        return self.request.user.orders.all()


class OrderProductListAPIView(ListAPIView):
    """
    APIView that lists user orders.
    """
    serializer_class = OrderProductSerializer
    queryset = OrderProduct.objects.none()
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('order__order_uuid', )
    ordering_fields = ('created_on', 'delivered_at', 'estimated_delivery_date',)
    filterset_fields = ('delivery_status', 'user', 'to_be_reviewed',)

    def get_queryset(self):
        if self.request.user.is_staff:
            return OrderProduct.objects.all()
        return self.request.user.ordered_products.all()


class MarkOrderAsCompletedAPIView(APIView):
    """
    APIView that marks order as completed and their corresponding ordered products
    and sets delivery date.
    """
    permission_classes = (IsAdminUser,)

    def post(self, request, *args, **kwargs):
        order_id = request.data.get('order_id', None)
        order_obj = get_order_obj(order_id)
        if order_obj.delivery_status=='Completed':
            return Response(
                {
                    'error_message': 'Order is already completed.'
                },
                status.HTTP_423_LOCKED
            )
        if order_obj.delivery_status=='Cancelled':
            return Response(
                {
                    'error_message': 'Order is already cancelled.'
                },
                status.HTTP_423_LOCKED
            )
        order_obj.delivery_status = 'Completed'
        order_obj.delivered_at = timezone.now().date()
        order_obj.save()

        order_obj.products.update(
            delivery_status='Completed',
            delivered_at = timezone.now().date()
        )

        for ordered_product in order_obj.products.all():
            Product.objects.filter(
                pk=ordered_product.product.pk
            ).update(
                quantity=F('quantity') - ordered_product.quantity, 
                items_sold=F('items_sold') + ordered_product.quantity
            )

        return Response(
            {
                'message': 'Marked order as completed.'
            },
            status.HTTP_200_OK
        )


class MarkOrderAsCancelledAPIView(APIView):
    """
    APIView that marks order as cancelled and their corresponding ordered products.
    """
    permission_classes = (IsAdminUser,)

    def post(self, request, *args, **kwargs):
        order_id = request.data.get('order_id', None)
        order_obj = get_order_obj(order_id)
        if order_obj.delivery_status=='Completed':
            return Response(
                {
                    'error_message': 'Order is already completed.'
                },
                status.HTTP_423_LOCKED
            )
        if order_obj.delivery_status=='Cancelled':
            return Response(
                {
                    'error_message': 'Order is already cancelled.'
                },
                status.HTTP_423_LOCKED
            )
        order_obj.delivery_status = 'Cancelled'
        order_obj.delivered_at = None
        order_obj.save()

        order_obj.products.update(
            delivery_status='Cancelled',
            delivered_at=None
        )

        return Response(
            {
                'message': 'Marked order as cancelled.'
            },
            status.HTTP_200_OK
        )


class PreOrderCheckOutCreateAPIView(CreateAPIView):
    """
    APIView that manages pre-order product bundle checkout and creates
    PreOrderProductBundle model instance.
    """
    serializer_class = PreOrderProductBundleSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {
                "message":"successfully pre-ordered."
            },
            status=status.HTTP_201_CREATED
        )

    def perform_create(self, serializer):

        payment_obj = serializer.validated_data.get('payment_obj')
        final_price = serializer.validated_data.get('final_price')
        shipping = serializer.validated_data.get('shipping')
        estimated_delivery_date = get_estimated_delivery_date(shipping.area.delivery_duration)
        product_bundle_obj = serializer.validated_data.get('product_bundle')

        pre_order_product_bundle_obj = PreOrderProductBundle.objects.create(
            user = self.request.user,
            product_bundle=product_bundle_obj,
            rate = product_bundle_obj.selling_price,
            payment = payment_obj,
            shipping = shipping,
            discount = serializer.validated_data.get('discount', 0),
            delivery_charge = serializer.validated_data.get('delivery_charge', 0),
            quantity = serializer.validated_data.get('quantity', 1),
            final_price = final_price,
            estimated_delivery_date = estimated_delivery_date
        )
        pre_order_product_bundle_obj.pre_order_uuid = generate_pre_order_uuid(pre_order_product_bundle_obj.pk)
        pre_order_product_bundle_obj.save()

        send_pre_order_create_mail_to_user(pre_order_product_bundle_obj)
        notify_user_about_pre_order_creation(pre_order_product_bundle_obj)
        notify_admin_about_pre_order_creation(pre_order_product_bundle_obj)

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'request': self.request,
        }


class PreOrderListAPIView(ListAPIView):
    """
    APIView that lists user pre-orders.
    """
    serializer_class = PreOrderProductBundleSerializer
    queryset = PreOrderProductBundle.objects.none()
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('pre_order_uuid', )
    ordering_fields = ('created_on', 'delivered_at')
    filterset_fields = ('delivery_status', 'user', 'product_bundle',)

    def get_queryset(self):
        if self.request.user.is_staff:
            return PreOrderProductBundle.objects.all()
        return self.request.user.pre_orders.all()


class MarkPreOrderAsCompletedAPIView(APIView):
    """
    APIView that marks pre-ordered product bundle as completed
    and sets delivery date.
    """
    permission_classes = (IsAdminUser,)

    def post(self, request, *args, **kwargs):
        pre_order_id = request.data.get('pre_order_id', None)
        pre_order_obj = get_pre_order_obj(pre_order_id)
        if pre_order_obj.delivery_status=='Completed':
            return Response(
                {
                    'error_message': 'Pre-Order is already completed.'
                },
                status.HTTP_423_LOCKED
            )
        if pre_order_obj.delivery_status=='Cancelled':
            return Response(
                {
                    'error_message': 'Pre-Order is already cancelled.'
                },
                status.HTTP_423_LOCKED
            )
        pre_order_obj.delivery_status = 'Completed'
        pre_order_obj.delivered_at = timezone.now().date()
        pre_order_obj.save()

        return Response(
            {
                'message': 'Marked pre-order as completed.'
            },
            status.HTTP_200_OK
        )


class MarkPreOrderAsCancelledAPIView(APIView):
    """
    APIView that marks pre-order as cancelled.
    """
    permission_classes = (IsAdminUser,)

    def post(self, request, *args, **kwargs):
        pre_order_id = request.data.get('pre_order_id', None)
        pre_order_obj = get_pre_order_obj(pre_order_id)
        if pre_order_obj.delivery_status=='Completed':
            return Response(
                {
                    'error_message': 'Pre-Order is already completed.'
                },
                status.HTTP_423_LOCKED
            )
        if pre_order_obj.delivery_status=='Cancelled':
            return Response(
                {
                    'error_message': 'pre-order is already cancelled.'
                },
                status.HTTP_423_LOCKED
            )
        pre_order_obj.delivery_status = 'Cancelled'
        pre_order_obj.delivered_at = None
        pre_order_obj.save()

        return Response(
            {
                'message': 'Marked pre-order as cancelled.'
            },
            status.HTTP_200_OK
        )


        












    









            
        


        









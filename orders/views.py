
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import (
    GenericAPIView,
    CreateAPIView,
    ListAPIView, 
    RetrieveAPIView
)
from rest_framework.views import APIView
from .models import (
    PromoCode,
    Order,
    OrderProduct,
)
from .serializers import (
    PromoCodeSerializer,
    OrderSerializer,
    OrderProductSerializer,
)
from .utils import (
    get_product_obj,
)

ORDER_PREFIX = 'NEBUYO-ORDER-'


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
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create_order(self, serializer):

        payment_obj = serializer.validated_data.get('payment_obj')
        final_price = serializer.validated_data.get('final_price')
        shipping = serializer.validated_data.get('shipping')

        order_obj = Order.objects.create(
            user = self.request.user,
            payment = payment_obj,
            shipping = shipping,
            discount = serializer.validated_data.get('discount', 0),
            delivery_charge = serializer.validated_data.get('delivery_charge', 0),
            final_price = final_price
        )
        order_obj.order_uuid = ORDER_PREFIX + str(order_obj.pk)
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
            )
    
    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'request': self.request,
        }


class UserOrderListAPIView(ListAPIView):
    """
    APIView that lists user orders.
    """
    serializer_class = OrderSerializer
    queryset = Order.objects.none()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('delivery_status',)

    def get_queryset(self):
        return self.request.user.orders.all()
    









            
        


        









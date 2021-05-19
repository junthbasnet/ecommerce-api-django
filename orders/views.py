
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import (
    GenericAPIView,
    ListAPIView, 
    RetrieveAPIView
)
from rest_framework.views import APIView
from .models import (
    PromoCode,
)
from .serializers import (
    PromoCodeSerializer,
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
            
        


        









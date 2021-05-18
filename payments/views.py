from decimal import Decimal
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets, filters
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .models import (
    # Payment,
    PaymentEnvironmentVariable,
)
from .serializers import (
    # IMEPaySerializer,
    # PaymentSerializer,
    EnvironmentVariableSerializer,
)
# from .verify_payment import (
#     verify_payment
# )
# from core.models import PaymentMethod


class PaymentEnvironmentVariableAPIViewSet(ModelViewSet):
    """
    APIViewSet to manage payment environment variables.
    """
    serializer_class = EnvironmentVariableSerializer
    permission_classes = (IsAdminUser,)
    queryset = PaymentEnvironmentVariable.objects.all()
    


# class IMEPayTokenCreateAPI(APIView):
#     """
#     Post Format :
#     {
#         "amount":5000
#     }
#     """
#     permission_classes = (IsAuthenticated,)
#     serializer_class = IMEPaySerializer

#     def post(self, request, *args, **kwargs):
#         user = request.user
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             serializer.save(user=user)
#         return Response(serializer.data, status.HTTP_201_CREATED)


# class CreatePaymentAPI(APIView):
#     """
#     Post Format :
#     {
#         "payment_method":"imepay",
#         "amount":100,
#         "RefId":"92230272-ecb8-4501-bc30-8995afdc6042",
#         "token":"2202102081645222232",
#         "TransactionId":"20210208-1657317326",
#         "Msisdn":"9846712371"
#     }
#     """
#     permission_classes = (IsAuthenticated,)

#     def post(self, request, *args, **kwargs):
#         payment_status = "unverified"
#         amount = Decimal(request.data.get('amount', 0.00))
#         if amount < 0:
#             return Response(
#                 {
#                     'message': 'Error in payment! Amount cant be zero'
#                 },
#                 status.HTTP_400_BAD_REQUEST
#             )
#         user = request.user
#         payment_method = request.data['payment_method']
#         try:
#             payment_method = PaymentMethod.objects.get(id=payment_method)
#         except :
#             return Response(
#                 {
#                     'message': 'Invalid Payment Method'
#                 }, status.HTTP_406_NOT_ACCEPTABLE
#                 )
#         status_code, currency = verify_payment(
#             user,
#             request.data,
#             payment_method.method_name.lower()
#         )

#         if status_code==407:
#             return Response(
#                 {
#                     'message': 'Insuccifient Funds'
#                 }, status.HTTP_400_BAD_REQUEST
#             )
#         elif status_code==426:
#             return Response(
#                 {
#                     'message': 'Duplicate Payment'
#                 }, status.HTTP_406_NOT_ACCEPTABLE
#             )
#         elif status_code==200:
#             payment_status="verified"
        
#         # For Testing Purpose only
#         if payment_method.method_name.lower()=='cod':
#             payment_status='unverified'

#         payment = Payment.objects.create(
#             method=payment_method,
#             payment_status=payment_status,
#             amount=amount,
#             user=user,
#             order_assigned=False,
#             status_code=status_code,
#             currency=currency
#         )
#         return Response(
#             {
#                 'message': 'Success',
#                 'data': PaymentSerializer(payment).data
#             },
#             status=status.HTTP_201_CREATED
#         )


# class UserPayment(viewsets.ReadOnlyModelViewSet):
#     queryset = Payment.objects.none()
#     serializer_class = PaymentSerializer
#     permission_classes = (IsAuthenticated,)
#     filter_backends = [DjangoFilterBackend, filters.SearchFilter]
#     filterset_fields = ['payment_status', 'method', ]
#     search_fields = ['method__name', ]

#     def get_queryset(self):
#         return self.request.user.user_payments.all()

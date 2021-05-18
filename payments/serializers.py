# from rest_framework import serializers

# from .models import IMEPay, Payment
# from orders.models import Order

# class IMEPaySerializer(serializers.ModelSerializer):
#     amount = serializers.IntegerField(min_value=1)

#     class Meta:
#         model = IMEPay
#         fields = ('id', 'ref_id', 'is_ref_id_available', 'amount', 'user')
#         read_only_fields = ('id', 'ref_id', 'is_ref_id_available', 'user', 'created_on', 'modified_on')


# class PaymentSerializer(serializers.ModelSerializer):
#     method_name = serializers.CharField(source='method.method_name', read_only=True)
#     course_title = serializers.SerializerMethodField(read_only=True)
#     class Meta:
#         model = Payment
#         fields = '__all__'
#         read_only_fields = (
#             'user',
#             'method',
#             'payment_status',
#             'amount',
#             'currency',
#             'payment_uuid',
#             'order_assigned',
#         )
#     def get_course_title(self, obj):
#         order = Order.objects.filter(payment=obj)
#         if order.exists():
#             name = order.first().course.title
#         else :
#             name = ""
#         return name

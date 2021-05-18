# from django.contrib import admin
# from .models import (
#     IMEPay,
#     KhaltiPayment,
#     FonepayPayment,
#     EsewaPayment,
#     CardPayment,
#     Payment,
# )

# @admin.register(IMEPay)
# class IMEPayAdmin(admin.ModelAdmin):
#     list_display = ('user', 'ref_id', 'is_ref_id_available',
#                     'amount')
#     list_filter = ('user', 'is_ref_id_available')
#     search_fields = ('user__email', 'amount', 'ref_id')


# @admin.register(KhaltiPayment)
# class KhaltiAdmin(admin.ModelAdmin):
#     list_display = ('user' ,'created_on', 'amount', 'status', 'token')
#     list_filter = ('status', 'user')
#     search_fields = ('token',)


# @admin.register(CardPayment)
# class CardPaymentAdmin(admin.ModelAdmin):
#     list_display = ('user', 'created_on', 'amount', 'transaction_id', 'req_reference_number', 'auth_trans_ref_no')
#     search_fields = ('amount', 'transaction_id', 'req_reference_number', 'auth_trans_ref_no', 'user')

# @admin.register(EsewaPayment)
# class EsewaAdmin(admin.ModelAdmin):
#     list_display = ('user', 'created_on', 'amount', 'pid', 'rid', 'status')
#     list_filter = ('status', 'user',)
#     search_fields = ('pid', 'ride')

# @admin.register(FonepayPayment)
# class FonepayAdmin(admin.ModelAdmin):
#     list_display = ('user', 'created_on', 'amount', 'status', 'bank', 'prn', 'bid', 'uid')
#     list_filter = ('status', 'user',)
#     search_fields = ('prn', )

# @admin.register(Payment)
# class PaymentAdmin(admin.ModelAdmin):
#     list_display = ('id', 'user', 'method', 'payment_uuid', 'payment_status', 'amount', 'currency', 'order_assigned', 'status_code')
#     list_filter = ('user', 'method', 'payment_status', 'currency', 'order_assigned', 'status_code')
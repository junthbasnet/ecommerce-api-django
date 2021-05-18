import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import BaseModel, TimeStampedModel


class PaymentEnvironmentVariable(TimeStampedModel):
    """
    Model to store payment environment variables.
    """
    key=models.CharField(_('key'), max_length=64, unique=True)
    value = models.CharField(_('value'), max_length=256, unique=True)

    class Meta:
        verbose_name = _('Payment Environment Variables')
        verbose_name_plural = _('Payment Environment Variables')
    
    def __str__(self):
        return f'{self.key}'



# class IMEPay(BaseModel):
#     user = models.ForeignKey('users.User', on_delete=models.SET_NULL, blank=True, null=True)
#     ref_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
#     is_ref_id_available = models.BooleanField(default=True)
#     amount = models.DecimalField(default=0, decimal_places=2, max_digits=10)

#     def __str__(self):
#         return f'{self.ref_id}-{self.is_ref_id_available}'


# class KhaltiPayment(BaseModel):
#     user = models.ForeignKey('users.User', on_delete=models.SET_NULL, blank=True, null=True)
#     token = models.CharField(max_length=200)
#     amount = models.CharField(max_length=100)
#     status = models.CharField(max_length=10)

#     class Meta:
#         ordering = ('-created_on',)


# class EsewaPayment(BaseModel):
#     user = models.ForeignKey('users.User', on_delete=models.SET_NULL, blank=True, null=True)
#     amount = models.CharField(max_length=100)
#     pid = models.CharField(max_length=50)
#     rid = models.CharField(max_length=50)
#     status = models.CharField(max_length=50)

#     class Meta:
#         ordering = ('-created_on',)


# class FonepayPayment(BaseModel):
#     user = models.ForeignKey('users.User', on_delete=models.SET_NULL, blank=True, null=True)
#     amount = models.CharField(max_length=100)
#     prn = models.CharField(max_length=100)
#     bid = models.CharField(max_length=100)
#     uid = models.CharField(max_length=100)
#     bank = models.CharField(max_length=100)
#     status = models.CharField(max_length=10)

#     class Meta:
#         ordering = ('-created_on',)


# class CardPayment(BaseModel):
#     user = models.ForeignKey('users.User', on_delete=models.SET_NULL, blank=True, null=True)
#     auth_trans_ref_no = models.CharField(max_length=255)
#     transaction_id = models.CharField(max_length=255)
#     req_reference_number = models.CharField(max_length=255)
#     amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     created_on = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f'{self.transaction_id}-{self.amount}'


# class Payment(BaseModel):
#     PAYMENT_STATUS = (
#         ('unverified', 'unverified'),
#         ('verified', 'verified'),
#     )
#     CURRENCY = (
#         ('NPR', 'NPR'),
#         ('USD', 'USD')
#     )
#     STATUS_CODES = (
#         ('CREATED', 'CREATED'),
#         ('MERCHANT_VERIFICATION_FAILED', 'MERCHANT_VERIFICATION_FAILED'),
#         ('NOT_FOUND', 'NOT_FOUND'),        
#     )
#     user = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, related_name='user_payments')
#     method = models.ForeignKey('core.PaymentMethod', on_delete=models.SET_NULL, null=True, related_name='method_payments')
#     payment_status = models.CharField(max_length=31, choices=PAYMENT_STATUS)
#     status_code = models.CharField(max_length=31, choices=STATUS_CODES, default='CREATED')
#     amount = models.DecimalField(default=0, decimal_places=2, max_digits=12)
#     currency = models.CharField(max_length=7, choices= CURRENCY, default='NPR')
#     payment_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
#     order_assigned = models.BooleanField(default=False, blank=True)

#     def __str__(self):
#         return f'Payment for {self.payment_uuid}'

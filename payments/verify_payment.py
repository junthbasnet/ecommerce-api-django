from payments.payment_verification_methods import (
    verify_imepay,
    verify_khalti,
    verify_esewa,
    verify_fonepay,
)
from decimal import Decimal
from payments import status


def verify_payment(user, data, payment_method):
    amount = Decimal(data['amount'])
    payment_status = "unverified"
    currency = 'NPR'
    # IMEPAY
    if payment_method == 'imepay':
        status_code = verify_imepay(user, data, amount)
    # Khalti
    elif payment_method == 'khalti':
        status_code = verify_khalti(user, data['token'], amount)
    # Esewa
    elif payment_method == 'esewa':
        status_code = verify_esewa(user, data, amount)
    # fonepay
    elif payment_method == 'fonepay':
        status_code = verify_fonepay(user, data, amount)
    # cod
    elif payment_method == 'cod':
        return status.PAYMENT_200_OK , currency
    else:
        status_code = status.PAYMENT_404_PAYMENT_METHOD_NOT_FOUND
    return status_code, currency

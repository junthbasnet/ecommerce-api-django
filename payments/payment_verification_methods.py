import json
import xml.etree.ElementTree as ET
import requests
from django.conf import settings

from .utils import generate_fonepay_hash
from payments.models import (
    IMEPay,
    KhaltiPayment,
    FonepayPayment,
    EsewaPayment,
)
from payments import status

def verify_fonepay(user, data, amount):
    amt = amount
    prn = data['prn']
    bid = data['bid']
    uid = data['uid']
    pid = settings.FONEPAY_MERCHANT_CODE
    if FonepayPayment.objects.filter(prn=prn).exists():
        return status.PAYMENT_426_DUPLICATE_PAYMENT
    dv = generate_fonepay_hash(pid, amt, prn, bid, uid)
    payload = {
        'PRN': prn,
        'PID': pid,
        'BID': bid,
        'AMT': amt,
        'UID': uid,
        'DV': dv
    }
    url = settings.FONEPAY_VERIFY_URL
    resp = requests.get(url, params=payload)
    string_xml = resp.content
    decoded = ET.fromstring(string_xml)
    verified_amount = decoded.find('txnAmount').text
    status_code = decoded.find('statusCode').text
    bank_code = decoded.find('bankCode').text
    if status_code =='1':
        status_code = status.PAYMENT_203_MERCHANT_VERIFICATION_FAILED
    else:
        status_code = status.PAYMENT_200_OK
    FonepayPayment.objects.create(
        amount=amt,
        prn=prn,
        bid=bid,
        uid=uid,
        bank=bank_code,
        status=status_code,
        user=user
    )
    return status_code


def verify_khalti(user, token, amount):
    payload = {
        "token": token,
        "amount": amount,
    }
    headers = {
        "Authorization": "Key {}".format(settings.KHALTI_SECRET_KEY)
    }
    if KhaltiPayment.objects.filter(token=token).exists():
        return status.PAYMENT_426_DUPLICATE_PAYMENT
    try:
        response = requests.post(settings.KHALTI_VERIFY_URL, payload,
                                 headers=headers)
        if response.status_code == 200:
            status_code = status.PAYMENT_200_OK
        else:
            status_code = status.PAYMENT_203_MERCHANT_VERIFICATION_FAILED
    except requests.exceptions.HTTPError as e:
        status_code = status.PAYMENT_203_MERCHANT_VERIFICATION_FAILED
    KhaltiPayment.objects.create(user=user, token=token, amount=amount, status=status_code)
    return status_code


def verify_esewa(user, data, amount):
    payload = {
        'amt': amount,
        'scd': settings.ESEWA_SCD,
        'rid': data['rid'],
        'pid': data['pid']
    }
    if EsewaPayment.objects.filter(pid=data['pid']).exists():
        return status.PAYMENT_426_DUPLICATE_PAYMENT

    try:
        response = requests.post(settings.ESEWA_VERIFY_URL, payload)

        if response.text.__contains__('Success'):
            status_code = status.PAYMENT_200_OK
        else:
            status_code = status.PAYMENT_203_MERCHANT_VERIFICATION_FAILED
    except requests.exceptions.HTTPError as e:
        status_code = status.PAYMENT_203_MERCHANT_VERIFICATION_FAILED

    EsewaPayment.objects.create(
        user=user,
        amount=amount,
        pid=data['pid'],
        rid=data['rid'],
        status=str(status_code)
    )
    return status_code


def verify_imepay(user, data, amount):
    url = settings.IME_URL
    MERCHANT_CODE = settings.IME_MERCHANT_CODE
    headers = {
        "Authorization": f"Basic {settings.IMEPAY_TOKEN}",
        "Module": settings.IME_MODULE
    }
    payload = {
        "MerchantCode": MERCHANT_CODE,
        "RefId": data['RefId'],
        "TokenId": data['token'],
        "TransactionId": data['TransactionId'],
        "Msisdn": data['Msisdn']
    }

    imepay = IMEPay.objects.filter(user=user, ref_id=data['RefId'],
                                   amount=amount,
                                   is_ref_id_available=True)

    if imepay.exists():
        ime = imepay.first()
        ime.is_ref_id_available = False
        ime.save()
        resp = requests.post(url, json.dumps(payload), headers=headers)
        resp = json.loads(resp.text)
        print(resp)
        if not resp['ResponseCode']:
            return status.PAYMENT_200_OK
        return status.PAYMENT_203_MERCHANT_VERIFICATION_FAILED
    return status.PAYMENT_404_PAYMENT_METHOD_NOT_FOUND
import datetime
import hashlib
import hmac
import math
import random
import time
import uuid
from base64 import b64encode
from django.conf import settings


def generate_fonepay_hash(pid, amt, prn, bid, uid):
    string = f'{pid},{amt},{prn},{bid},{uid}'
    string = string.encode('utf-8')
    hmac_hash = hmac.new(key=b'f8f89c75a5164ae3a391ddc35222804d', msg=string,
                         digestmod=hashlib.sha512)
    return hmac_hash.hexdigest()


def generate_fonepay_hash_frontend(pid, md, prn, amt, crn, dt, r1, r2, ru):
    string = f'{pid},{md},{prn},{amt},{crn},{dt},{r1},{r2},{ru}'
    string = string.encode('utf-8')
    hmac_hash = hmac.new(key=b'f8f89c75a5164ae3a391ddc35222804d',
                         msg=string, digestmod=hashlib.sha512)
    return hmac_hash.hexdigest()


def msTimeStamp():
    return int(round(time.time() * 1000))


def generate_random():
    characters = '0123456789'
    result = ''
    for i in range(20):
        result += characters[math.floor(random.random() * len(characters))]
    return result


def generate_hash_cybersource(amt):
    transaction_uuid = uuid.uuid4()
    signed_date_time = str(datetime.datetime.utcnow().isoformat(timespec='seconds')) + 'Z'
    reference_number = msTimeStamp()
    auth_trans_ref_no = generate_random()
    signed_fields_name = "access_key,profile_id,transaction_uuid,signed_field_names,unsigned_field_names,signed_date_time,locale,transaction_type,reference_number,amount,currency,payment_method,bill_to_forename,bill_to_surname,bill_to_email,bill_to_phone,bill_to_address_line1,bill_to_address_city,bill_to_address_state,bill_to_address_country,bill_to_address_postal_code,auth_trans_ref_no"
    field_values = ["access_key" + "=" + settings.CYBERSOURCE_ACCESS_KEY,
                    "profile_id" + "=" + settings.CYBERSOURCE_PROFILE_ID,
                    "signed_field_names" + "=" + signed_fields_name,
                    "unsigned_field_names" + "=" + "card_type,card_number,card_expiry_date",
                    "signed_date_time" + "=" + signed_date_time,
                    "transaction_uuid" + "=" + str(transaction_uuid),
                    "locale" + "=" + "en",
                    "transaction_type" + "=" + "sale",
                    "reference_number" + "=" + str(reference_number),
                    "amount" + "=" + str(amt),
                    "currency" + "=" + "USD",
                    "bill_to_forename" + "=" + "Puran",
                    "bill_to_surname" + "=" + "Ban",
                    "bill_to_email" + "=" + "aashishdhakal7@gmail.com",
                    "bill_to_phone" + "=" + "9865383233",
                    "bill_to_address_line1" + "=" + "N/A",
                    "bill_to_address_city" + "=" + "N/A",
                    "bill_to_address_state" + "=" + "N/A",
                    "bill_to_address_country" + "=" + "NP",
                    "bill_to_address_postal_code" + "=" + "N/A",
                    "auth_trans_ref_no" + "=" + str(reference_number),
                    ]
    string = ",".join(field_values)
    hmac_hash = hmac.new(key=settings.CYBERSOURCE_SECRET_KEY.encode(),
                         msg=string.encode(),
                         digestmod=hashlib.sha256).digest()
    return b64encode(hmac_hash).decode(), transaction_uuid, reference_number, \
           signed_date_time, auth_trans_ref_no, string



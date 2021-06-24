import firebase_admin
from django.conf import settings
from firebase_admin import credentials, auth
from firebase_admin.auth import verify_id_token

from .models import User

cred = credentials.Certificate(str(settings.FIREBASE_KEY_PATH))
default_app = firebase_admin.initialize_app(cred)


def validate_id_token(id_token):
    decoded = verify_id_token(id_token)
    uuid = decoded.get('uid')
    email = decoded.get('email')
    try:
        profile_pic = decoded.get('photoURL')
    except :
        profile_pic = None
    phone_number = decoded.get('phoneNumber')
    if uuid and email:
        user, created = User.objects.get_or_create(email=email)
        if created:
            # need to save other fields too
            user.firebase_uuid = uuid
            if profile_pic:
                user.profile_pic = profile_pic
            user.phone_number = phone_number
            user.save()
    else:
        user = None
    return user


def delete_user_by_provider_id(provider_id, delete_request):
    print("Called")
    page = auth.list_users()
    user_found = False
    while page:
        for user in page.users:
            if user.provider_data[0].uid==provider_id:
                print("User Found")
                try:
                    user_db = User.objects.get(email=user.email)
                    user_db.is_active = False
                    delete_request.user = user_db
                    delete_request.status = "completed"
                    delete_request.save()
                    user_db.save()
                except User.DoesNotExist:
                    pass
                auth.delete_user(user.uid)
                break
        if user_found:
            break
        page = page.get_next_page()

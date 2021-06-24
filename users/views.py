import base64
import json
import hmac
import hashlib
from decouple import config
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, mixins
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import  ListCreateAPIView
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    AllowAny,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from .helpers import delete_user_by_provider_id
from .models import (
    Shipping,
    FacebookDataDelete,
)
from .permissions import (
    IsOwnerOrReadOnly,
)
from .serializers import (
    UserAuthTokenSerializer,
    UserSerializer,
    UserRegisterSerializer,
    ShippingSerializer
)

User = get_user_model()


class UserAPIViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)
    queryset = User.objects.all()
    http_method_names = ['get', 'put', 'patch', ]
    filter_backends = [DjangoFilterBackend,SearchFilter]
    filterset_fields = ['is_active', 'is_staff',]
    search_fields = ['full_name','email','phone_number']


    @action(methods=['PUT'], detail=True, url_path='remove-admin-status')
    def remove_admin_status(self, request, pk):
        user = self.get_object()
        user.is_staff = False
        user.is_superuser = False
        user.save()
        return Response(
            {
                'message':"Admin Status Removed"
            }, status.HTTP_202_ACCEPTED)

    @action(methods=['PUT'], detail=True, url_path='promote-to-admin')
    def promote_to_admin(self, request, pk):
        user = self.get_object()
        user.is_staff = True
        user.is_superuser = False
        user.save()
        return Response(
            {
                'message':"Promoted to Admin"
            }, status.HTTP_202_ACCEPTED)

    @action(methods=['PUT'], detail=True, url_path='promote-to-superuser')
    def promote_to_superuser(self, request, pk):
        user = self.get_object()
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return Response(
            {
                'message':"Promoted to Superuser"
            }, status.HTTP_202_ACCEPTED)


class UserProfileAPIViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.none()
    http_method_names = ['get', 'put', 'patch', ]

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)

    def paginate_queryset(self, queryset):
        return None


class RegisterUserAPIView(APIView):
    """
    API View for registration.
    """
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        data = UserSerializer(user).data
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                'message': 'Success',
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': data,
            },
            status.HTTP_201_CREATED
        )


class ObtainAuthTokenView(ObtainAuthToken):
    serializer_class = UserAuthTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        try:
            email = serializer.initial_data['username']
            user = get_object_or_404(User, email=email)
            if not user.is_active:
                return Response(
                    {
                        'message': 'You account is currently under review. It will be activated real soon by Homework Team.'
                    },
                    status.HTTP_200_OK
                )
        except:
            pass
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        user_serializer = UserSerializer(user)
        return Response(
            {
                'message': 'Success',
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': user_serializer.data
            },
            status.HTTP_200_OK
        )


class ShippingAPIViewSet(viewsets.ModelViewSet):
    """
    Viewset to add, update, list and delete shippings of logged in user.
    """
    serializer_class = ShippingSerializer
    queryset = Shipping.objects.none()
    permission_classes = (
        IsAuthenticated,
    )

    def get_queryset(self):
        return self.request.user.shippings.all()

    def perform_create(self, serializer):
        is_default = serializer.validated_data.get('is_default')
        if is_default:
            self.get_queryset().update(is_default=False)
        serializer.save(user=self.request.user)
    
    def perform_update(self, serializer):
        if serializer.validated_data.get('is_default'):
            self.get_queryset().exclude(pk=self.kwargs.get('pk')).update(is_default=False)
        serializer.save()


class TokenCheckAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        return Response(
            {
                'message':'Token Valid'
            },
            status.HTTP_200_OK
        )


class CheckUserDeletionStatus(APIView):
    permission_classes = (AllowAny, )

    def get(self, request, *args, **kwargs):
        try:
            f_del=FacebookDataDelete.objects.get(uuid=request.GET.get('user'))
            return HttpResponse(f'Your data deletion process is {f_del.status}')
        except :
            return HttpResponse(f'Invalid Request')


class FacebookDataDeletion(APIView):
    permission_classes = (AllowAny, )

    def post(self, request, *args, **kwargs):
        signed_request = request.data['signed_request']
        encoded_sig, payload = signed_request.split('.')
        fb_secret = config("FACEBOOK_SECRET")
        sig = base64.urlsafe_b64decode(encoded_sig+'==')
        data = base64.urlsafe_b64decode(payload+'==').decode("utf-8")
        expected_sig = hmac.new(key=fb_secret.encode("utf-8"), msg=payload.encode('utf-8'),digestmod=hashlib.sha256).digest()
        if (sig != expected_sig):
            return Response({'message': 'Not Found'}, status.HTTP_400_BAD_REQUEST)
        delete_request = FacebookDataDelete.objects.create(status="initiated")
        data=json.loads(data)
        delete_user_by_provider_id(data['user_id'], delete_request)
        return Response(
            {
                'url': f'http://3.15.39.153/api/users/check-status/?user={delete_request.uuid}',
                'confirmation_code': delete_request.uuid
            },
            status.HTTP_200_OK
        )
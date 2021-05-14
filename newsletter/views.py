from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from newsletter.helpers import random_digits
from newsletter.models import Newsletter, Subscriber
from newsletter.serializers import NewsletterSerializer, SubscriberSerializer
from newsletter.tasks import send_subscription_email


class SubscriberViewset(ModelViewSet):
    permission_classes = (IsAdminUser,)
    serializer_class = SubscriberSerializer
    queryset = Subscriber.objects.all()
    http_method_names = ('get', 'delete')


class NewsletterViewset(ModelViewSet):
    permission_classes = (IsAdminUser,)
    serializer_class = NewsletterSerializer
    queryset = Newsletter.objects.all()
    filter_backends = [SearchFilter, ]
    search_fields = ['title', 'email_subject']

    def create(self, request):
        serializer = NewsletterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'message': 'Successfully Added New Campaign',
                    'data': serializer.data
                },
                status.HTTP_201_CREATED
            )
        else:
            return Response(serializer.errors, status=400)

    def update(self, request, *args, **kwargs):
        ns = self.get_object()
        serializer = NewsletterSerializer(ns, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'message': 'Successfully Edited Campaign',
                    'data': serializer.data
                },
                status.HTTP_200_OK
            )
        else:
            return Response(serializer.errors, status=400)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            name = instance.title
            self.perform_destroy(instance)
        except Http404:
            return Response(
                {
                    'message': 'No Such Campaign'
                },
                status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                'message': f'{name} Deleted Successfully'
            },
            status.HTTP_200_OK
        )


class SubscribeAPI(APIView):
    '''
    {
        "email":"ajaykarki333@gmail.com"
    }
    '''
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SubscriberSerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            obj.code = obj.email.split('@')[0] + str(random_digits())
            obj.save()
            return Response(
                {
                    'message': 'Successfully Subscribed'
                },
                status.HTTP_200_OK
            )
        return Response(serializer.errors, status=400)


class UnsubscribeAPI(APIView):
    """
    api for unsubscribing user
    :param
    email
    code
    http://localhost:8000/api/v1/newsletter/unsubscribe/?email=ajaykarki33@gmail.com&code=ajaykarki33793632841798
    """
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        email = self.request.query_params.get('email')
        code = self.request.query_params.get('code')
        try:
            sub = Subscriber.objects.get(email=email)
            if sub.code == code:
                sub.delete()
                return Response(
                    {
                        'status': True,
                        'detail': 'Unsubscribed Successfully'
                    },
                    status.HTTP_200_OK
                )
            return Response(
                {
                    'status': False,
                    'detail': 'Email and Code not matched.',
                },
                status.HTTP_400_BAD_REQUEST
            )
        except Subscriber.DoesNotExist:
            return Response(
                {
                    'status': False,
                    'detail': 'Email does not exist.',
                },
                status.HTTP_400_BAD_REQUEST
            )


class SendSubsriptionMailAPI(APIView):
    permission_classes = (IsAdminUser,)

    def post(self, request, id):
        subscribers = Subscriber.objects.all()
        if not subscribers.exists():
            return Response(
                {
                    'message': 'Failed there are no subscribers'
                },
                status.HTTP_400_BAD_REQUEST
            )
        try:
            newsletter = Newsletter.objects.get(id=id)
        except ObjectDoesNotExist:
            return Response(
                {
                    'message': 'Invalid newsletter'
                },
                status.HTTP_400_BAD_REQUEST
            )
        subscribers = SubscriberSerializer(subscribers, many=True).data
        newsletter = NewsletterSerializer(newsletter).data

        send_subscription_email.delay(subscribers, newsletter)
        return Response(
            {
                'message': 'Mail is being sent'
            },
            status.HTTP_200_OK
        )

from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import Notification
from .serializers import NotificationSerializer


class NotificationAPI(ModelViewSet):
    queryset = Notification.objects.none()
    serializer_class = NotificationSerializer
    http_method_names = ['get', ]
    permission_classes = [permissions.IsAuthenticated, ]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    @action(methods=['get'], detail=True, url_path='mark-as-read')
    def mark_as_read(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.is_read = True
        obj.save()
        return Response(
            {
                'message': 'Marked as read'
            },
            status.HTTP_200_OK
        )

    @action(methods=['get'], detail=True, url_path='mark-as-unread')
    def mark_as_unread(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.is_read = True
        obj.save()
        return Response(
            {
                'message': 'Marked as unread'
            },
            status.HTTP_200_OK
        )


class MarkAllAsReadAPI(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        notifications = Notification.objects.filter(user=request.user, is_read=False)
        for noti in notifications:
            noti.is_read = True
            noti.save()
        return Response(
            {
                'message': 'Marked all as read'
            },
            status.HTTP_200_OK
        )

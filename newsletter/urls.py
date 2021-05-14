from django.urls import path, include

from newsletter.views import (
    SubscribeAPI,
    UnsubscribeAPI,
    SendSubsriptionMailAPI)
from .routers import router

app_name = 'newsletter'

urlpatterns = [
    path('', include(router.urls)),
    path('subscribe/', SubscribeAPI.as_view()),
    path('unsubscribe/', UnsubscribeAPI.as_view()),
    path('send-subscription-mail/<int:id>/', SendSubsriptionMailAPI.as_view())

]

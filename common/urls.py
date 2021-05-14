from django.urls import path, include

from .routers import router

app_name = 'common'

urlpatterns = [
    path('', include(router.urls)),
]

from django.urls import path, include
from .routers import router

app_name = 'products'

urlpatterns = [
    path('', include(router.urls)),
]

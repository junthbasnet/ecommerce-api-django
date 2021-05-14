from django.urls import path, include

from .routers import router

app_name = 'blog'

urlpatterns = [
    path('', include(router.urls)),
]

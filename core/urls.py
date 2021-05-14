from django.urls import path, include

from .routers import router
from .views import SEOSettingsAPI, SiteSettingsAPI

app_name = 'core'

urlpatterns = [
    path('', include(router.urls)),
    path('seo-settings/', SEOSettingsAPI.as_view(), name='seo_settings'),
    path('site-settings/', SiteSettingsAPI.as_view(), name='site_settings'),
]

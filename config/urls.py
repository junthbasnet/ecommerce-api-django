from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from core.views import home_view

apipatterns = (
    [
        path('users/', include('users.urls')),
        path('common/', include('common.urls')),
        path('blogs/', include('blog.urls')),
        path('core/', include('core.urls')),
        path('newsletter/', include('newsletter.urls')),
        path('notifications/', include('notifications.urls')),
        path('products/', include('products.urls')),
    ], 'api')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', include_docs_urls(title="Nebuyo API", description="Nebuyo API Docs")),
    path('api/', include(apipatterns)),
    path('', home_view),
    path('summernote/', include('django_summernote.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
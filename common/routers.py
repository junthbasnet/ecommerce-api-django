from rest_framework.routers import DefaultRouter

from .views import (
    FileUploadAPIViewSet,
    GetFileForUserAPI
)

router = DefaultRouter()
router.register('file-upload', FileUploadAPIViewSet)
router.register('get-files-for-user', GetFileForUserAPI)

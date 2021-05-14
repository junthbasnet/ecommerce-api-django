from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .models import FileUpload
from .serializers import FileUploadSerializer


class FileUploadAPIViewSet(ModelViewSet):
    serializer_class = FileUploadSerializer
    queryset = FileUpload.objects.none()

    def get_queryset(self, *args, **kwargs):
        try:
            return self.request.user.file_uploads.all()
        except:
            return []

    def create(self, request, *args, **kwargs):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            user = None
            if request.user.is_authenticated:
                user = request.user
            file = serializer.save(user=user)
            media_url = request.build_absolute_uri(file.file.url)
            return Response(
                {
                    'media_url': media_url,
                },
                status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class GetFileForUserAPI(ReadOnlyModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FileUploadSerializer
    queryset = FileUpload.objects.none()

    def get_queryset(self):
        return FileUpload.objects.filter(user=self.request.user)

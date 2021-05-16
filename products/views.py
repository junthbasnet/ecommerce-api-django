from django.db.models import ProtectedError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import (
    Category,
    SubCategory,
    Product,
    ProductColor,
    ProductImage,
    GlobalSpecification,
)
from .serializers import (
    CategorySerializer,
)


class CategoryAPIViewSet(ModelViewSet):
    """
    APIViewset to manage product categories.
    """
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


    def destroy(self, request, *args, **kwargs):
        """
        Destroy a model instance.
        """
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
        except ProtectedError:
            return Response(
                {
                    'message': 'Cannot delete category. Delete all its sub-categories and products first.'
                },
                status.HTTP_406_NOT_ACCEPTABLE
            )
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()















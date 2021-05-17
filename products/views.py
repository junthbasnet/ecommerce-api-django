from django.db.models import ProtectedError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import (
    Brand,
    Category,
    SubCategory,
    Product,
    ProductImage,
    GlobalSpecification,
)
from .serializers import (
    CategorySerializer,
    SubCategorySerializer,
    ProductSerializer,
    GlobalSpecificationSerializer,
    BrandSerializer,
    ProductImageSerializer,
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


class SubCategoryAPIViewSet(ModelViewSet):
    """
    APIViewset to manage product sub-categories.
    """
    serializer_class = SubCategorySerializer
    queryset = SubCategory.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = (
        'name', 'description', 'slug', 'category__name', 'category__description',
    )
    filterset_fields = ('category', 'category__slug',)

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
                    'message': 'Cannot delete sub-category. Delete all its products first.'
                },
                status.HTTP_406_NOT_ACCEPTABLE
            )
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()


class ProductAPIViewSet(ModelViewSet):
    """
    APIViewSet to manage products.
    """
    serializer_class = ProductSerializer
    queryset = Product.objects.all().order_by('-id')
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = (
        'name', 'overview', 'slug', 'sub_category__name',
        'sub_category__description',
    )
    filterset_fields = (
        'sub_category', 'sub_category__slug', 'sub_category__category',
        'sub_category__category__slug', 'brand', 
    )


class GlobalSpecificationAPIViewSet(ModelViewSet):
    """
    APIViewSet to manage global product specification.
    """
    serializer_class = GlobalSpecificationSerializer
    queryset = GlobalSpecification.objects.all()


class BrandAPIViewSet(ModelViewSet):
    """
    APIViewSet to manage product brands.
    """
    serializer_class = BrandSerializer
    queryset = Brand.objects.all()


class ProductImageAPIViewSet(ModelViewSet):
    """
    APIViewSet to manage product images.
    """
    serializer_class = ProductImageSerializer
    queryset = ProductImage.objects.all()

















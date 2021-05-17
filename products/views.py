
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import ProtectedError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from .models import (
    Brand,
    Category,
    SubCategory,
    Product,
    ProductImage,
    GlobalSpecification,
    Question,
    Answer,
)
from .serializers import (
    CategorySerializer,
    SubCategorySerializer,
    ProductSerializer,
    GlobalSpecificationSerializer,
    BrandSerializer,
    ProductImageSerializer,
    ProductQuestionSerializer,
    ProductAnswerSerializer,
)
from .utils import (
    get_similar_products,
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


class ProductQuestionAPIViewSet(ModelViewSet):
    """
    APIViewSet to manage product questions.
    """
    serializer_class = ProductQuestionSerializer
    queryset = Question.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('product', 'is_answered',)


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProductAnswerAPIViewSet(ModelViewSet):
    """
    APIViewSet to manage product answers.
    """
    serializer_class = ProductAnswerSerializer
    queryset = Answer.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('question', )

    def perform_create(self, serializer):
        answer_obj = serializer.save(user=self.request.user)
        answer_obj.question.is_answered=True
        answer_obj.question.save()


class CompareSimilarProductsListAPIView(ListAPIView):
    """
    APIView that returns list of similar products for comparision.
    """
    serializer_class = ProductSerializer
    queryset = Product.objects.none()

    def list(self, request, *args, **kwargs):
        product_id = request.GET.get('product_id', None)
        if product_id:
            try:
                product_obj = Product.objects.get(pk=product_id)
            except ObjectDoesNotExist:
                return Response(
                    {
                        'message':'Object doesn\'t exist'
                    },
                    status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {
                    'message':'Please provide product_id.'
                },
                status.HTTP_406_NOT_ACCEPTABLE
            )
        
        query = product_obj.name
        queryset = get_similar_products(query)[:4]        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class SimilarProductsListAPIView(ListAPIView):
    """
    APIView that returns similar products.
    """
    serializer_class = ProductSerializer
    queryset = Product.objects.none()

    def list(self, request, *args, **kwargs):
        product_id = request.GET.get('product_id', None)
        if product_id:
            try:
                product_obj = Product.objects.get(pk=product_id)
            except ObjectDoesNotExist:
                return Response(
                    {
                        'message':'Object doesn\'t exist'
                    },
                    status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {
                    'message':'Please provide product_id.'
                },
                status.HTTP_406_NOT_ACCEPTABLE
            )
        
        query = product_obj.name
        similar_products = get_similar_products(query)
        queryset = similar_products[4:9]
        if len(queryset) <= 5:
            queryset = list(similar_products)[-1::-1]        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)





    



    

















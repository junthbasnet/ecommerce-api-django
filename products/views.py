
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import ProtectedError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Avg, Max, Min
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
)
from .models import (
    Brand,
    Category,
    SubCategory,
    Product,
    ProductImage,
    GlobalSpecification,
    Question,
    Answer,
    RatingAndReview,
    DealOfTheDay,
)
from .permissions import(
    IsOwnerOrReadOnly,
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
    RatingAndReviewSerializer,
    DealOfTheDaySerializer,
)
from .utils import (
    get_similar_products,
    get_ordered_product_obj,
    get_product_obj,
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
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = (
        'name', 'overview', 'slug', 'sub_category__name',
        'sub_category__description',
    )
    filterset_fields = (
        'sub_category', 'sub_category__slug', 'sub_category__category',
        'sub_category__category__slug', 'brand', 
    )
    ordering_fields = (
        'items_sold', 'selling_price', 'created_on',
        'views_count', 'average_rating',
    )

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a model instance and increase views_count by 1.
        """
        instance = self.get_object()
        instance.views_count += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


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


class RatingAndReviewAPIViewSet(ModelViewSet):
    """
    APIViewSet that manages ratings and reviews.
    """
    serializer_class = RatingAndReviewSerializer
    queryset = RatingAndReview.objects.all()
    permission_classes = (IsOwnerOrReadOnly,)
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = ('user', 'product',)
    search_fields = ('review', 'user',)
    ordering_fields = ['created_on',]
    
    def create(self, request, *args, **kwargs):
        ordered_product_id = request.data.get('ordered_product_id')
        ordered_product_obj = get_ordered_product_obj(ordered_product_id)
        if ordered_product_obj.user != request.user:
            return Response(
                {
                    'error_message': 'You cannot give review unless you order a product.'
                },
                status.HTTP_405_METHOD_NOT_ALLOWED
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['ordered_product_obj'] = ordered_product_obj
        if ordered_product_obj.reviews:
            return Response(
                {
                    'error_message':'Already reviewed. only update'
                },
                status.HTTP_418_IM_A_TEAPOT
            )       
        self.perform_create(serializer)
        return Response(
            {
                'message':'successfully reviewed.'
            }
            ,status=status.HTTP_201_CREATED
        )

    def perform_create(self, serializer):
        ordered_product_obj = serializer.validated_data.get('ordered_product_obj')
        review_obj = RatingAndReview.objects.create(
            user=self.request.user,
            product = ordered_product_obj.product,
            rating=serializer.validated_data.get('rating', 5),
            review = serializer.validated_data.get('review'),
            image = serializer.validated_data.get('image')
        )         
        ordered_product_obj.reviews = review_obj
        ordered_product_obj.to_be_reviewed=False
        ordered_product_obj.save()

        self.set_average_rating(ordered_product_obj.product)
    
    def set_average_rating(self, product_obj):
        average_rating = product_obj.reviews.aggregate(average_rating=Avg('rating')).get('average_rating', 5)
        product_obj.average_rating = average_rating
        product_obj.save()
        print(average_rating)

    def perform_update(self, serializer):
        serializer.save()
        product_obj = self.get_object().product
        self.set_average_rating(product_obj)
    
    def perform_destroy(self, instance):
        instance.on_ordered_product.to_be_reviewed=True
        instance.on_ordered_product.save()
        instance.delete()
        product_obj = instance.product
        self.set_average_rating(product_obj)


class MarkProductAsFeaturedAPIView(APIView):
    """
    APIView that marks product as featured.
    """
    permission_classes = (IsAdminUser,)

    def post(self, request, *args, **kwargs):
        product_id = request.data.get('product_id', None)
        product_obj = get_product_obj(product_id)

        Product.objects.update(is_featured=False)
        product_obj.is_featured=True
        product_obj.save()
        
        return Response(
            {
                'message': f'sets {product_obj.name} as featured product.'
            },
            status.HTTP_200_OK
        )


class DealOfTheDayProductAPIViewSet(ModelViewSet):
    """
    APIViewSet that manages deal of the day products.
    """
    serializer_class = DealOfTheDaySerializer
    queryset = DealOfTheDay.objects.none()

    def get_queryset(self):
        return DealOfTheDay.objects.filter(
            start_date__lte=timezone.now().date(),
            end_date__gte=timezone.now().date()
        )
    



    





    



    


















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
    IsAuthenticatedOrReadOnly,
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
    PopularPick,
    ProductForPreOrder,
    ProductBundleForPreOrder,
    ProductBanner,
    FeaturedProduct,
    Offer,
)
from .filters import ProductFilterSet
from .permissions import(
    IsOwnerOrReadOnly,
    IsAdminUserOrReadOnly,
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
    PopularPickSerializer,
    ProductForPreOrderSerializer,
    ProductBundleForPreOrderSerializer,
    ProductBannerSerializer,
    FeaturedProductSerializer,
    OfferSerializer,
)
from .utils import (
    get_similar_products,
    get_ordered_product_obj,
    get_product_obj,
)
from .recommender import Recommender


class CategoryAPIViewSet(ModelViewSet):
    """
    APIViewset to manage product categories.
    """
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = (IsAdminUserOrReadOnly,)


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
    permission_classes = (IsAdminUserOrReadOnly,)
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
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = (
        'name', 'overview', 'slug', 'sub_category__name',
        'sub_category__description',
    )
    filterset_class = ProductFilterSet
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
    permission_classes = (IsAdminUser,)


class BrandAPIViewSet(ModelViewSet):
    """
    APIViewSet to manage product brands.
    """
    serializer_class = BrandSerializer
    queryset = Brand.objects.all()
    permission_classes = (IsAdminUserOrReadOnly,)


class ProductImageAPIViewSet(ModelViewSet):
    """
    APIViewSet to manage product images.
    """
    serializer_class = ProductImageSerializer
    queryset = ProductImage.objects.all()
    permission_classes=(IsAdminUser,)


class ProductQuestionAPIViewSet(ModelViewSet):
    """
    APIViewSet to manage product questions.
    """
    serializer_class = ProductQuestionSerializer
    queryset = Question.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
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
    permission_classes = (IsAdminUserOrReadOnly,)
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
        
        queryset = get_similar_products(product_obj)      
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
        
        similar_products = get_similar_products(product_obj)
        queryset = similar_products        
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
        average_rating = average_rating if average_rating else 5
        product_obj.average_rating = average_rating
        product_obj.save()

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


class FeaturedProductAPIViewSet(ModelViewSet):
    """
    APIViewSet that manages featured product.
    """
    serializer_class = FeaturedProductSerializer
    queryset = FeaturedProduct.objects.all().order_by('-id')
    permission_classes = (IsAdminUserOrReadOnly,)

    def perform_create(self, serializer):
        """
        Creates featured product and resets all other set featured products.
        """
        self.set_featured_product(serializer)
    
    def perform_update(self, serializer):
        """
        Updates featured product and resets all other set featured products.
        """
        self.set_featured_product(serializer)

    def set_featured_product(self, serializer):
        FeaturedProduct.objects.all().delete()
        Product.objects.update(is_featured=False)
        
        featured_product_obj = serializer.save()
        featured_product_obj.product.is_featured=True
        featured_product_obj.product.save()


class DealOfTheDayProductAPIViewSet(ModelViewSet):
    """
    APIViewSet that manages deal of the day products.
    query-params = deal-of-the-day
    possible_values : ['active', 'inactive', 'expired', 'upcoming']
    """
    serializer_class = DealOfTheDaySerializer
    queryset = DealOfTheDay.objects.all()
    permission_classes=(IsAdminUserOrReadOnly,)
    filter_backends = (OrderingFilter,)
    ordering_fields = ['created_on', 'priority']

    def get_queryset(self):
        queryset = self.queryset 
        query_params = self.request.GET.get('deal-of-the-day')
        if query_params == 'active':
            queryset= DealOfTheDay.objects.filter(
                start_date__lte=timezone.now().date(),
                end_date__gte=timezone.now().date()
            )
        if query_params == 'inactive':
            queryset= DealOfTheDay.objects.exclude(
                start_date__lte=timezone.now().date(),
                end_date__gte=timezone.now().date()
            )      
        if query_params == 'expired':
            queryset= DealOfTheDay.objects.filter(
                end_date__lt=timezone.now().date()
            )      
        if query_params == 'upcoming':
            queryset= DealOfTheDay.objects.filter(
                start_date__gt=timezone.now().date()
            )      
        return queryset
    
        def get_serializer_context(self):
            """
            Extra context provided to the serializer class.
            """
            return {
                'request': self.request,
            }


class TodaysPopularPickProductAPIViewSet(ModelViewSet):
    """
    APIViewSet that manages today's popular pick products.
    """
    serializer_class = PopularPickSerializer
    queryset = PopularPick.objects.all()
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ('is_active',)
    ordering_fields = ['created_on', 'priority']

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'request': self.request,
        }


class ProductForPreOrderAPIViewSet(ModelViewSet):
    """
    APIViewSet that manages products for pre-order.
    """
    serializer_class = ProductForPreOrderSerializer
    queryset = ProductForPreOrder.objects.all()
    permission_classes = (IsAdminUser,)


class ProductBundleForPreOrderAPIViewSet(ModelViewSet):
    """
    APIViewSet that manages product bundles for pre-order.
    """
    serializer_class = ProductBundleForPreOrderSerializer
    queryset = ProductBundleForPreOrder.objects.all()
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ('is_active',)
    ordering_fields = ['created_on',]

    def perform_create(self, serializer):
        """
        Creates Product bundle model instances and sets description.
        """
        self.perform_set_description(serializer)

    def perform_update(self, serializer):
        """
        Updates Product bundle model instances and sets description.
        """
        self.perform_set_description(serializer)
    
    def perform_set_description(self, serializer):
        product_bundle_obj = serializer.save()
        products = serializer.validated_data.get('products')
        description = 'Contains '
        for i, product in enumerate(products):
            if i == 0:
                description += f'{product.name}'
            elif i == len(products) -1:
                description += f', and {product.name}'
            else:
                description += f', {product.name}'
        product_bundle_obj.description = description
        product_bundle_obj.save()


class ProductBannerAPIViewSet(ModelViewSet):
    """
    APIViewSet that manages product banners.
    """
    serializer_class = ProductBannerSerializer
    queryset = ProductBanner.objects.all()
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (OrderingFilter,)
    ordering_fields = ('created_on', 'priority',)


class OfferAPIViewSet(ModelViewSet):
    """
    APIViewSet that manages offers (Dashain Offer).
    query-params = offers
    possible_values : ['active', 'inactive', 'expired', 'upcoming']
    """
    serializer_class = OfferSerializer
    queryset = Offer.objects.all()
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    filterset_fields=('is_deleted',)
    ordering_fields = ['created_on',]

    def get_queryset(self):
        queryset = self.queryset 
        query_params = self.request.GET.get('offers')
        if query_params == 'active':
            queryset= Offer.objects.filter(
                start_date__lte=timezone.now().date(),
                end_date__gte=timezone.now().date()
            )
        if query_params == 'inactive':
            queryset= Offer.objects.exclude(
                start_date__lte=timezone.now().date(),
                end_date__gte=timezone.now().date()
            )      
        if query_params == 'expired':
            queryset= Offer.objects.filter(
                end_date__lt=timezone.now().date()
            )      
        if query_params == 'upcoming':
            queryset= Offer.objects.filter(
                start_date__gt=timezone.now().date()
            )      
        return queryset
    
        def get_serializer_context(self):
            """
            Extra context provided to the serializer class.
            """
            return {
                'request': self.request,
            }


class ProductBoughtTogetherAPIView(APIView):
    """
    APIView that returns products that are bought together.
    """
    def post(self, request, *args, **kwargs):
        product_ids = request.data.get('product_ids', None)
        if product_ids is None:
            return Response(
                {
                    'error':'product_ids is required.'
                },
                status.HTTP_400_BAD_REQUEST
            )

        top_selling_products = Product.objects.order_by('-items_sold')
        if product_ids == []:
            return Response(
                {
                    'data': ProductSerializer(top_selling_products, many=True).data
                },
                status.HTTP_200_OK
            )
            
        recommender = Recommender()
        suggested_products, suggested_products_ids = recommender.suggest_products_for(product_ids)
        suggested_products += top_selling_products.exclude(id__in=suggested_products_ids)
        return Response(
            {
                'data': ProductSerializer(suggested_products, many=True).data,
            },
            status.HTTP_200_OK
        )


class RecommendedProductsAPIView(APIView):
    """
    APIView that returns recommended products according to what the user has bought
    previously, otherwise top selling products.
    """
    def get(self, request, *args, **kwargs):
        user = self.request.user
        top_selling_products = Product.objects.order_by('-items_sold')
        if user.is_anonymous:
            return Response(
                {
                    'data': ProductSerializer(top_selling_products, many=True).data
                }
            )

        product_ids = user.ordered_products.values_list('product', flat=True)
        if product_ids == []:
            return Response(
                {
                    'data': ProductSerializer(top_selling_products, many=True).data
                },
                status.HTTP_200_OK
            )
        
        recommender = Recommender()
        suggested_products, suggested_products_ids = recommender.suggest_products_for(product_ids)
        suggested_products += top_selling_products.exclude(id__in=suggested_products_ids)
        return Response(
            {
                'data': ProductSerializer(suggested_products, many=True).data,
            },
            status.HTTP_200_OK
        )
        
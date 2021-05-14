from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets, status
from rest_framework.response import Response

from common.permissions import IsAdminUserOrReadOnly
from .models import (
    BlogCategory,
    Article,
)
from .serializers import (
    BlogCategorySerializer,
    ArticleSerializer,
)


class CategoryAPI(viewsets.ModelViewSet):
    """
    Category Listing API
    """
    permission_classes = (IsAdminUserOrReadOnly,)
    serializer_class = BlogCategorySerializer
    queryset = BlogCategory.objects.all()

    def paginate_queryset(self, queryset):
        if self.paginator and self.request.query_params.get(self.paginator.page_query_param, None) is None:
            return None
        return super().paginate_queryset(queryset)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'message': 'Successfully Added Category',
                    'data': serializer.data
                },
                status.HTTP_201_CREATED
            )
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(obj, data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            return Response(
                {
                    'message': 'Successfully Edited Category',
                    'data': serializer.data
                },
                status.HTTP_200_OK
            )
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        name = instance.title
        self.perform_destroy(instance)
        return Response(
            {
                'message': f'{name} Deleted Successfully'
            },
            status.HTTP_204_NO_CONTENT
        )


class ArticleAPI(viewsets.ModelViewSet):
    """
    Article Listing API
    search param:
        Category Title
    Filter param: 
        Category ID
    Ordering Param:
        views
    """
    permission_classes = (IsAdminUserOrReadOnly,)
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['category__title', 'title']
    filterset_fields = ('category', 'author')
    ordering_fields = ['views', 'created_at']

    def retrieve(self, request, pk):
        article = self.get_object()
        session_key = 'viewed_article_{}'.format(article.id)
        if not request.session.get(session_key, False):
            article.views += 1
            article.save()
            request.session[session_key] = True
        return Response(ArticleSerializer(article).data)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(
                {
                    'message': 'Successfully Added Article',
                    'data': serializer.data
                },
                status.HTTP_201_CREATED
            )
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(obj, data=request.data)
        if not (obj.author == request.user):
            return Response(
                {
                    'message': 'Unauthorized User !'
                }, status.HTTP_403_FORBIDDEN
            )
        if serializer.is_valid():
            obj = serializer.save()
            return Response(
                {
                    'message': 'Successfully Edited Article',
                    'data': serializer.data
                },
                status.HTTP_200_OK
            )
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        name = instance.name
        self.perform_destroy(instance)
        return Response(
            {
                'message': f'{name} Deleted Successfully'
            },
            status.HTTP_204_NO_CONTENT
        )

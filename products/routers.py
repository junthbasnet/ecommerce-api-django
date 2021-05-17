from rest_framework.routers import DefaultRouter

from .views import (
    BrandAPIViewSet,
    CategoryAPIViewSet,
    GlobalSpecificationAPIViewSet,
    ProductAPIViewSet,
    ProductImageAPIViewSet,
    SubCategoryAPIViewSet,
    ProductQuestionAPIViewSet,
    ProductAnswerAPIViewSet,
)

router = DefaultRouter()

router.register('categories', CategoryAPIViewSet)
router.register('sub-categories', SubCategoryAPIViewSet)
router.register('brands', BrandAPIViewSet)
router.register('specifications', GlobalSpecificationAPIViewSet)
router.register('images', ProductImageAPIViewSet)
router.register('questions', ProductQuestionAPIViewSet)
router.register('answers', ProductAnswerAPIViewSet)
router.register('', ProductAPIViewSet)


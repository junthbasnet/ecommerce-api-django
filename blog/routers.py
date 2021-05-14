from rest_framework.routers import DefaultRouter

from .views import (
    CategoryAPI,
    ArticleAPI,
)

router = DefaultRouter()
router.register('categories', CategoryAPI)
router.register('articles', ArticleAPI)

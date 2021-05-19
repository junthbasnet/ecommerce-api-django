from rest_framework.routers import DefaultRouter

from .views import (
    SocialLinkViewSet,
    SlideShowViewSet,
    FAQCategoryViewSet,
    FAQViewSet,
    PaymentMethodViewSet,
    TestimonialViewSet,
    ProvinceAPIViewSet,
    CityAPIViewSet,
    AreaAPIViewSet,
)

router = DefaultRouter()
router.register('social-links', SocialLinkViewSet)
router.register('slideshow', SlideShowViewSet)
router.register('faq-category', FAQCategoryViewSet)
router.register('faq', FAQViewSet)
router.register('payment-methods', PaymentMethodViewSet)
router.register('testimonial', TestimonialViewSet)
router.register('province', TestimonialViewSet)
router.register('cities', TestimonialViewSet)
router.register('areas', TestimonialViewSet)
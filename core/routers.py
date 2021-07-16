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
    PageWiseSEOSettingViewset,
    SiteSettingAPIViewSet,
)


router = DefaultRouter()
router.register('social-links', SocialLinkViewSet)
router.register('slideshow', SlideShowViewSet)
router.register('faq-category', FAQCategoryViewSet)
router.register('faq', FAQViewSet)
router.register('payment-methods', PaymentMethodViewSet)
router.register('testimonial', TestimonialViewSet)
router.register('province', ProvinceAPIViewSet)
router.register('cities', CityAPIViewSet)
router.register('areas', AreaAPIViewSet)
router.register('page-seo-settings', PageWiseSEOSettingViewset)
router.register('site-settings', SiteSettingAPIViewSet)
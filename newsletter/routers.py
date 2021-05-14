from rest_framework.routers import DefaultRouter

from newsletter.views import NewsletterViewset,SubscriberViewset

router = DefaultRouter()

router.register('newsletters', NewsletterViewset)
router.register('subscribers', SubscriberViewset)

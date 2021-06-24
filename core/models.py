from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from common.models import (
    SEOBaseModel,
    TimeStampedModel,
    BaseModel,
    Category
)
from common.managers import DefaultManager
from common.utils import compress


class SiteSetting(models.Model):
    site_icon = models.ImageField(null=True, blank=True, upload_to='settings')
    site_title = models.CharField(max_length=255, blank=True)
    contact_number = models.CharField(max_length=25, default="", blank=True)
    address = models.CharField(max_length=255, default="", blank=True)
    email = models.EmailField(default="admin@akku.gg", blank=True)

    def __str__(self):
        return self.site_title

    def save(self, *args, **kwargs):
        if self.site_icon:
            new_image = compress(self.site_icon)
            self.site_icon = new_image
        super().save(*args, **kwargs)


class SEOSetting(SEOBaseModel):
    def __str__(self):
        return self.og_title


class PageWiseSEOSetting(TimeStampedModel):
    page_title = models.CharField(max_length=200)
    route = models.CharField(max_length=200)
    og_url = models.URLField(blank=True, default="https://nebuyo.com/")
    og_title = models.CharField(max_length=255, blank=True, default="")
    og_description = models.TextField(blank=True, default="")
    og_image = models.ImageField(upload_to='seo-uploads', null=True, blank=True)
    meta_title = models.CharField(max_length=255, default="", blank=True)
    meta_description = models.TextField(default="", blank=True)
    keywords = models.TextField(default="", blank=True)
    tags = models.TextField(default="", blank=True)

    class Meta:
        verbose_name=_('Page-Wise SEO Setting')
        verbose_name_plural=_('Page-Wise SEO Setting')
        ordering=('created_on',)


class SocialLinkSetting(models.Model):
    icon = models.ImageField(null=True, blank=True, upload_to='settings')
    platform = models.CharField(max_length=255)
    link = models.URLField()

    def __str__(self):
        return f"{self.platform}-{self.link}"

    def save(self, *args, **kwargs):
        if self.icon:
            new_image = compress(self.icon)
            self.icon = new_image
        super().save(*args, **kwargs)


class PaymentMethod(TimeStampedModel):
    method_name = models.CharField(_('method name'), max_length=128, unique=True)
    slug = models.CharField(_('slug'), max_length=128, unique=True)
    charge = models.PositiveIntegerField(
        _('charge'),
        default=0,
        help_text=_('charge that gets added up during checkout.')
    )
    icon = models.ImageField(null=True, blank=True, upload_to='payment_methods')
    priority = models.PositiveIntegerField(
        _('priority'),
        default=0,
        help_text=_('Higher the priority, first it comes in listing.')
    )

    class Meta:
        verbose_name = _('Payment Method')
        verbose_name_plural = _('Payment Methods')
        ordering = ('-priority',)

    def __str__(self):
        return f'{self.method_name}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.method_name)
        if self.icon:
            new_image = compress(self.icon)
            self.icon = new_image
        super().save(*args, **kwargs)


class Slideshow(TimeStampedModel):
    image = models.ImageField(upload_to='content-images')
    link = models.URLField()
    caption = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Slideshow'
        verbose_name_plural = 'Slideshow'


class FAQCategory(Category):
    class Meta:
        verbose_name = 'FAQ Category'
        verbose_name_plural = 'FAQ Categories'


class FAQ(TimeStampedModel):
    category = models.ForeignKey(FAQCategory, on_delete=models.CASCADE, null=True, default=None, related_name='faqs')
    question = models.CharField(max_length=200, unique=True)
    answer = models.TextField()
    slug = models.SlugField(max_length=255, default="", unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.question

    def save(self, *args, **kwargs):
        self.slug = slugify(self.question)
        super(FAQ, self).save(*args, **kwargs)


class Testimonial(models.Model):
    full_name = models.CharField(max_length=255)
    info = models.CharField(max_length=255)
    profile_image = models.ImageField(upload_to='uploads/testimonials', max_length=500)
    description = models.TextField()

    def __str__(self):
        return self.full_name


class Province(TimeStampedModel):
    """
    Model to store Province information for shipping.
    """
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name='Province'
        verbose_name_plural = 'Province'
        ordering = ('-created_on',)


class City(TimeStampedModel):
    """
    Model to store city information for shipping charges.
    """
    name = models.CharField(max_length=255, unique=True)
    province = models.ForeignKey(
        Province,
        on_delete=models.PROTECT,
        related_name="cities",
    )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'
        ordering = ('-created_on',)


class Area(TimeStampedModel):
    """
    Model to store city information for shipping.
    """
    name = models.CharField(max_length=255, unique=True)
    city = models.ForeignKey(
        City,
        on_delete=models.PROTECT,
        related_name="areas",
    )
    delivery_duration = models.PositiveIntegerField(default=3)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name='Area'
        verbose_name_plural = 'Areas'
        ordering = ('-created_on',)

        
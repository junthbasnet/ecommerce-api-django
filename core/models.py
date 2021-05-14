from django.db import models
from django.utils.text import slugify

from common.models import SEOBaseModel, TimeStampedModel, BaseModel, Category
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
    method_name = models.CharField(max_length=100)
    charge = models.PositiveIntegerField(help_text='Charge')
    icon = models.ImageField(null=True, blank=True, upload_to='settings')

    def __str__(self):
        return f'{self.method_name} Charge: {self.charge}'

    def save(self, *args, **kwargs):
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
import os
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.db.models import Avg, Max, Min
from django.utils import timezone

from common.models import SEOBaseModel, TimeStampedModel


class Category(SEOBaseModel):
    """
    Product Category
    """
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(default='')
    image = models.ImageField(upload_to='categories', null=True, blank=True)
    priority  = models.PositiveIntegerField(
        default=0,
        blank=True,
        help_text=_('Higher the priority, first it comes in listing'),
    )

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ('-priority',)
    
    def __str__(self):
        return f'{self.name}'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    
class SubCategory(SEOBaseModel):
    """
    Product Subcategory
    """
    category = models.ForeignKey(
        'Category',
        on_delete=models.PROTECT,
        related_name='sub_categories'
    )
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(default='')
    image = models.ImageField(upload_to='sub-categories',null=True, blank=True)

    class Meta:
        verbose_name = _('Sub-Category')
        verbose_name_plural = _('Sub-Categories')
    
    def __str__(self):
        return f'{self.name}'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Brand(models.Model):
    """
    Product brand
    """
    name = models.CharField(_('name'), max_length=64, unique=True)
    slug = models.CharField(_('slug'), max_length=64, unique=True)
    image = models.ImageField(_('image'), upload_to='brands')
    
    class Meta:
        verbose_name = _('Brand')
        verbose_name_plural = _('Brands')
    
    def __str__(self):
        return f'{self.name}'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(SEOBaseModel):
    """
    Model to store product information.
    """
    name = models.CharField(_('name'), max_length=255, unique=True)
    slug = models.CharField(_('slug'), max_length=255, unique=True)
    sub_category = models.ForeignKey(
        'SubCategory',
        on_delete=models.PROTECT,
        related_name='products'
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        related_name='brand_products',
    )
    quantity = models.PositiveIntegerField(default=0)
    items_sold = models.PositiveIntegerField(default=0)

    marked_price = models.DecimalField(
        _('marked price'),
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(1)]
    )
    selling_price = models.DecimalField(
        _('selling price'),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(1)]
    )

    overview = models.TextField(default='')
    specifications = models.JSONField(default=dict)

    hero_image = models.ImageField(_('hero image'), upload_to='products/hero-image/', default=None)
    images = models.JSONField(_('images'), default=list)
    color_images = models.JSONField(_('color images'), default=list)

    average_rating = models.DecimalField(
        _('average rating'),
        max_digits=3,
        decimal_places=2,
        default=5,
        null=True,
        help_text=_(
            'average rating calculated from ratings and reviews table.'
        )
    )
    views_count = models.PositiveIntegerField(
        _('views count'),
        default=0,
        help_text=_(
            'number of times the product is viewed.'
        )
    )

    is_featured = models.BooleanField(_('is featured'), default=False)


    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
    
    def __str__(self):
        return f'{self.name}'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def count_of_users_who_rated(self):
        return self.reviews.count()

    @property
    def is_deal_of_the_day(self):
        try:
            return True if self.deal_of_the_day and self.deal_of_the_day.is_valid else False
        except:
            return False

    @property
    def is_todays_popular_pick(self):
        try:
            return True if self.todays_popular_pick and self.todays_popular_pick.is_active else False
        except:
            return False


class FeaturedProduct(TimeStampedModel):
    """
    Model to store featured product.
    """
    product = models.OneToOneField(
        'Product',
        on_delete=models.CASCADE,
        related_name='featured',
    )
    
    class Meta:
        verbose_name = _('Featured Product')
        verbose_name_plural = _('Featured Product')


class DealOfTheDay(TimeStampedModel):
    """
    Model to store deal of the day products.
    """
    product = models.OneToOneField(
        'Product',
        on_delete=models.CASCADE,
        related_name='deal_of_the_day',
    )
    start_date = models.DateField(_('start date'))
    end_date = models.DateField(_('end date'))
    priority  = models.PositiveIntegerField(
        default=0,
        blank=True,
        help_text=_('Higher the priority, first it comes in listing'),
    )
    
    class Meta:
        verbose_name = _('Deal Of The Day')
        verbose_name_plural = _('Deal Of The Day')
        ordering = ('-priority',)
    
    @property
    def is_valid(self):
        return self.start_date <= timezone.now().date() <= self.end_date


class PopularPick(TimeStampedModel):
    """
    Model to store today's popular pick products.
    """
    product = models.OneToOneField(
        'Product',
        on_delete=models.CASCADE,
        related_name='todays_popular_pick',
    )
    is_active = models.BooleanField(_('is active'), default=True)
    priority  = models.PositiveIntegerField(
        default=0,
        blank=True,
        help_text=_('Higher the priority, first it comes in listing'),
    )
    
    class Meta:
        verbose_name = _('Today\'s Popular Pick')
        verbose_name_plural = _('Today\'s Popular Pick')
        ordering = ('-priority',)


class GlobalSpecification(TimeStampedModel):
    """
    Model to store product specification keys.
    """
    name = models.CharField(_('name'), max_length=255, unique=True)
    slug = models.CharField(_('slug'), max_length=255, unique=True)

    class Meta:
        verbose_name = _('Global Specification')
        verbose_name_plural = _('Global Specifications')

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    
class ProductImage(models.Model):
    """
    Product images.
    """
    image = models.ImageField(_('image'), upload_to='products/images/', default=None)

    class Meta:
        verbose_name = _('Product Image')
        verbose_name_plural = _('Product Images')


class Question(TimeStampedModel):
    """
    Model to store product specific question.
    """
    user = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='user_questions'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='questions',
    )
    question = models.TextField()
    is_answered = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Question')
        verbose_name_plural = _('Questions')
        ordering = ('-created_on', )
    
    def __str__(self):
        return f'{self.question[:20]}... asked by {self.user}'


class Answer(TimeStampedModel):
    """
    Model to store answer for product specific questions.
    """
    user = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='user_answers'
    )
    question = models.OneToOneField(Question, on_delete=models.CASCADE)
    answer = models.TextField()

    class Meta:
        verbose_name = _('Answer')
        verbose_name_plural = _('Answers')
        ordering = ('-created_on', )
    
    def __str__(self):
        return f'{self.answer[:20]}... asked by {self.user}'


class RatingAndReview(TimeStampedModel):
    """
    Model to store ratings and reviews on ordered products.
    """
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    rating = models.PositiveIntegerField(
        _('rating'),
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    review = models.TextField(_('review'))
    image = models.ImageField(_('image'), upload_to='product_reviews')

    class Meta:
        verbose_name = _('Ratings & Reviews')
        verbose_name_plural = _('Ratings & Reviews')
        ordering = ('-created_on',)


class ProductForPreOrder(TimeStampedModel):
    """
    Model to store pre-order products for bundling them.
    """
    name = models.CharField(_('name'), max_length=255)
    image = models.ImageField(_('image'), upload_to='products_for_pre_order')

    class Meta:
        verbose_name = _('Product For Pre-Order')
        verbose_name_plural = _('Products For Pre-Order')
        ordering = ('-created_on',)
    
    def __str__(self):
        return f'{self.name}'


class ProductBundleForPreOrder(SEOBaseModel):
    """
    Model that stores pre order product bundles.
    """
    name = models.CharField(_('name'), max_length=255)
    slug = models.SlugField(_('slug'), max_length=255)
    image = models.ImageField(_('image'), upload_to='product_bundles_for_pre_order')
    products = models.ManyToManyField('ProductForPreOrder', related_name='product_bundles')
    description = models.CharField(
        _('description'),
        max_length=512,
        default='',
        help_text=_('short description of what this bundle contains.')
    )
    overview = models.TextField(_('overview'), default='')
    marked_price = models.DecimalField(
        _('marked price'),
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(1)]
    )
    selling_price = models.DecimalField(
        _('selling price'),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(1)]
    )
    is_active = models.BooleanField(_('is_active'), default=True)

    class Meta:
        verbose_name = _('Product Bundle For Pre-Order')
        verbose_name_plural = _('Product Bundles For Pre-Order')
        ordering = ('-created_on',)
    
    def __str__(self):
        return f'{self.name}'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ProductBanner(TimeStampedModel):
    """
    Model to store product secondary banners
    """
    title = models.CharField(_('title'), max_length=255,)
    image = models.ImageField(_('image'), upload_to='products/secondary_banner/')
    redirect_link = models.URLField(_('redirect link'))
    priority  = models.PositiveIntegerField(
        default=0,
        blank=True,
        help_text=_('Higher the priority, first it comes in listing'),
    )

    class Meta:
        verbose_name = _('Product Secondary Banner')
        verbose_name_plural = _('Product Secondary Banner')
        ordering = ('-priority', '-created_on',)
    
    def __str__(self):
        return f'{self.title}'
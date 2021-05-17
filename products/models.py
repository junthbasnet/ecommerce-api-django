import os
from django.db import models
from django.core.validators import MinValueValidator
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

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

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
    
    def __str__(self):
        return f'{self.name}'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


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






    











    









    







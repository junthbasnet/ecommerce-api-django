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
    brand = models.CharField(
        _('brand'),
        max_length=255,
        help_text=_('brand the product belongs to (eg. JBL)'),
    )
    quantity = models.PositiveIntegerField(default=0)
    items_sold = models.PositiveIntegerField(default=0)

    marked_price = models.DecimalField(
        _('marked price'),
        max_digits=10,
        decimal_places=2,
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
    image = models.ImageField(_('Image'), upload_to='products/%Y/%m/%d/', default=None)

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
    
    def __str__(self):
        return f'{self.name}'


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


class ProductColor(TimeStampedModel):
    name = models.CharField(_('name'), max_length=31)
    code = models.CharField(_('color code'), max_length=15)
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        related_name='colors'
    )

    class Meta:
        verbose_name = _('Product Color')
        verbose_name_plural = _('Product Color')
        constraints = [
            models.UniqueConstraint(fields=['name', 'product'], name='unique_colors')
        ]
    











    









    







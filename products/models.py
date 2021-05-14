from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from common.models import SEOBaseModel


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




    







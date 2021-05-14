from django.db import models
from django.utils.text import slugify

from common.models import SEOBaseModel, Category


class BlogCategory(Category):
    class Meta:
        verbose_name = 'Blog Category'
        verbose_name_plural = 'Blog Categories'


class Article(SEOBaseModel):
    title = models.CharField(max_length=500)
    slug = models.SlugField()
    category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to='thumbnails', blank=True, null=True)
    description = models.TextField()
    author = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='blogs')
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-created_on',)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Article, self).save(*args, **kwargs)

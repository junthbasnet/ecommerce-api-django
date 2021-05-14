from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import (
    BlogCategory,
    Article,
)


class CategoryAdmin(SummernoteModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}
    exclude = ['modified_on', 'created_on', ]


class ArticleAdmin(SummernoteModelAdmin):
    list_display = ['title', 'category', 'created_on', ]
    list_filter = ['category', ]
    search_fields = ['title', ]
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ['description', ]
    readonly_fields = ["views", ]


admin.site.register(BlogCategory, CategoryAdmin)
admin.site.register(Article, ArticleAdmin)

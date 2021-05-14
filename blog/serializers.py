from rest_framework import serializers

from .models import (
    BlogCategory,
    Article,
)


class BlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = '__all__'
        read_only_fields = ('slug',)


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        exclude = (
            'modified_on',
            'created_on',
        )
        read_only_fields = ('slug', 'author', 'views')

from django_filters import rest_framework as filters
from django_filters.widgets import CSVWidget
from .models import Product, SubCategory, Brand


class ProductFilterSet(filters.FilterSet):
    min_avg_rating = filters.NumberFilter(field_name="average_rating", lookup_expr='gte')
    selling_price = filters.RangeFilter(field_name="selling_price",)
    sub_category = filters.ModelMultipleChoiceFilter(
        field_name='sub_category',
        queryset=SubCategory.objects.all(),
        widget=CSVWidget,
    )
    brand = filters.ModelMultipleChoiceFilter(
        field_name='brand',
        queryset=Brand.objects.all(),
        widget=CSVWidget,
    )

    class Meta:
        model = Product
        fields = (
            'sub_category', 'sub_category__slug', 'sub_category__category',
            'sub_category__category__slug', 'brand', 'selling_price',
            'min_avg_rating', 'is_featured',
        )
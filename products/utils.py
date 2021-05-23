from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from rest_framework import serializers
from django.contrib.postgres.search import (
    SearchVector,
    SearchQuery,
    SearchRank
)
from .models import Product
from orders.models import OrderProduct


def get_similar_products(query):
    """
    Returns similar products.
    """
    search_vector = (
        SearchVector('name', weight='A') +
        SearchVector('overview', weight='B')
    )
    search_query = SearchQuery(query)
    queryset = (
        Product.objects.annotate(
            rank=SearchRank(search_vector, search_query)
        )
        .order_by('-rank')
    )
    return queryset


def get_ordered_product_obj(ordered_product_id):
    """
    Raises validation error or returns ordered_product_obj.
    """
    try:
        ordered_product_obj = OrderProduct.objects.get(pk=ordered_product_id)
    except ObjectDoesNotExist or MultipleObjectsReturned:
        raise serializers.ValidationError(
            {
                'error_message': [
                    f"Product with ordered_product_id:{ordered_product_id} doesn't exist."
                ]
            },
            code='invalid_ordered_product_id'
        )
    return ordered_product_obj


def get_product_obj(product_id):
    """
    Raises validation error or returns product_obj.
    """
    try:
        product_obj = Product.objects.get(pk=product_id)
    except ObjectDoesNotExist or MultipleObjectsReturned:
        raise serializers.ValidationError(
            {
                'error_message': [
                    f"Product with product_id:{product_id} doesn't exist."
                ]
            },
            code='invalid_product_id'
        )
    return product_obj
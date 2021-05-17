from django.contrib.postgres.search import (
    SearchVector,
    SearchQuery,
    SearchRank
)
from .models import Product

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
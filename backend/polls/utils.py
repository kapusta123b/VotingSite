from django.db import connection
from django.db.models import Q
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

def q_search(query, queryset):
    vector = SearchVector(
        "creator__username",
        "question_text",
        "id"
    )
    
    search_query = SearchQuery(query)

    result = queryset.annotate(rank=SearchRank(vector, search_query)).filter(rank__gt=0).order_by("-rank")
    
    return result
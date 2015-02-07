from rest_framework import filters

class TwitterUserFilterBackend(filters.BaseFilterBackend):
    """
    Filter that only allows users to see their own objects.
    """
    def filter_queryset(self, request, queryset, view):
        twitter_id = request.QUERY_PARAMS.get('twitter_id', None)
        if twitter_id is not None:
            queryset = queryset.filter(twitter_id=twitter_id)
        return queryset
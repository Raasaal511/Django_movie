from django_filters import rest_framework as filter
from movie.models import Movie


class CharFilterInFilter(filter.BaseInFilter, filter.CharFilter):
    pass


class MovieFilter(filter.FilterSet):
    genres = CharFilterInFilter(filter_name='genre__name', lookup_expr='in')
    year = filter.RangeFilter()

    class Meta:
        model = Movie
        fields = ['genres', 'year']

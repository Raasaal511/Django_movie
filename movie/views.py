from django.views.generic import ListView, DetailView

from .models import Movie, Genre, Category
from django.db.models import Q

from .utils import DataMixin


class GenreYear:

    def get_genre(self):
        return Genre.objects.all()

    def get_year(self):
        return Movie.objects.filter(is_published=True).values('year')


class MovieView(DataMixin, GenreYear, ListView):
    """Фильмы"""
    model = Movie
    context_object_name = 'movies'

    def get_context_data(self, *, object_list=None, **kwargs):
        # получаем категрии и жанры фильмов
        context = super().get_context_data(**kwargs)
        context_mixin = self.get_context_data_mixin()

        return dict(list(context.items()) + list(context_mixin.items()))


class MovieDetailView(DataMixin, GenreYear, DetailView):
    """О фильме"""
    model = Movie
    slug_field = 'slug'
    context_object_name = 'movies_detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context_mixin = self.get_context_data_mixin()

        return dict(list(context.items()) + list(context_mixin.items()))


class MovieCategoryView(DataMixin, GenreYear, ListView):
    model = Movie
    template_name = 'movie/movie_category.html'
    slug_field = 'slug'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context_mixin = self.get_context_data_mixin()

        return dict(list(context.items()) + list(context_mixin.items()))

    def get_queryset(self):
        category_queryset = Movie.objects.filter(category__slug=self.kwargs.get('slug'))

        return category_queryset


class FilterMovieView(GenreYear, DataMixin, ListView):
    model = Movie

    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist('year')) |
            Q(genre__in=self.request.GET.getlist('genre'))
        )

        return queryset

from django.urls import path

from . import views

urlpatterns = [
    path('', views.MovieView.as_view(), name='movie'),
    path('category/<slug:slug>/', views.MovieCategoryView.as_view(), name='category'),
    path('filter/', views.FilterMovieView.as_view(), name='filter'),
    path('<slug:slug>/', views.MovieDetailView.as_view(), name='movie_detail'),
]

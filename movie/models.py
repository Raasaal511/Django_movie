from datetime import date

from django.db import models
from django.urls import reverse


class Genre(models.Model):
    name = models.CharField(max_length=155)
    description = models.TextField()
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Actor(models.Model):
    """ Актеры """
    name = models.CharField(max_length=100)
    age = models.PositiveSmallIntegerField(verbose_name='Возраст', default=0)
    description = models.TextField('Описание')
    photo = models.ImageField(upload_to='actors_photo/', null=True, blank=True)

    def __str__(self):
        return f'Name{self.name}, Age:{self.age},'

    class Meta:
        verbose_name = 'Актер'
        verbose_name_plural = 'Актеры'


class Movie(models.Model):
    """ Фильмы """
    genre = models.ManyToManyField(Genre, verbose_name='Жанры')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    poster = models.ImageField(upload_to='movies/', blank=True, null=True)
    description = models.TextField()
    director = models.ManyToManyField(Actor, verbose_name='Режиссер', related_name='film_director')
    actors = models.ManyToManyField(Actor, related_name='film_actor')
    country = models.CharField(max_length=155, verbose_name='Страна')
    budget = models.PositiveIntegerField(verbose_name='Бюджет',
                                         default=0, help_text='Указывать сумму в долларах')
    fees_in_usa = models.PositiveIntegerField('Сборы в США',
                                              default=0, help_text='Указывать сумму в долларах')
    fees_in_word = models.PositiveIntegerField('Сборы в Мире',
                                               default=0, help_text='Указывать сумму в долларах')
    release = models.DateField(default=date.today, verbose_name='Примьера в мире')
    year = models.PositiveSmallIntegerField(default=0)
    is_published = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'

        ordering = ['-id']

    def get_absolute_url(self):
        return reverse('movie_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name


class MovieShots(models.Model):
    """ Кадры из фильма """
    title = models.CharField('Заголовок', max_length=100)
    description = models.TextField('Описание')
    image = models.ImageField(upload_to='movie_shots/', null=True, blank=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Кадр из фильма'
        verbose_name_plural = 'Кадры из фильма'


class StarRating(models.Model):
    """ Звезды ретинга """
    value = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.value

    class Meta:
        verbose_name = 'Звезда ретинга'
        verbose_name_plural = 'Звезды ретинга'


class Rating(models.Model):
    """ Ретинги """
    ip = models.CharField('IP адрес', max_length=15)
    star = models.ForeignKey(StarRating, on_delete=models.CASCADE, verbose_name='Звезда')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name='Фильм')

    def __str__(self):
        return f'{self.ip}: {self.star}, movie:{self.movie}'

    class Meta:
        verbose_name = 'Ретинг'
        verbose_name_plural = 'Ретинги'


class Reviews(models.Model):
    """ Отзывы """
    email = models.EmailField()
    name = models.CharField(max_length=255)
    text = models.TextField(max_length=5000)
    parent = models.ForeignKey('self', verbose_name='Родитель',
                               on_delete=models.SET_NULL, blank=True, null=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name='Фильм')

    def __str__(self):
        return f'{self.name} - {self.movie}'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

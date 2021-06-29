from .models import Category, Genre


class DataMixin:
    def get_context_data_mixin(self, **kwargs):
        context = kwargs
        context['categories'] = Category.objects.all()
        context['genres'] = Genre.objects.all()

        return context

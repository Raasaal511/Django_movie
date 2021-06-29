from django.contrib import admin
from . import models as md



@admin.register(md.Movie)
class MovieAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('name', 'category')}


admin.site.register(md.Rating)
admin.site.register(md.MovieShots)
admin.site.register(md.Category)
admin.site.register(md.Actor)
admin.site.register(md.Genre)
admin.site.register(md.Reviews)
admin.site.register(md.StarRating) 
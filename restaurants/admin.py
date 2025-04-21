from django.contrib import admin

from restaurants.models import Commentaire, Log, Restaurant, TypeResto

# Register your models here.

admin.site.register(Restaurant)
admin.site.register(TypeResto)
admin.site.register(Commentaire)
admin.site.register(Log)
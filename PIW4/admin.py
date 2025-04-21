from django.contrib import admin

from restaurants.models import Commentaire, Restaurant, TypeResto

# Register your models here.

admin.site.register(Restaurant)
admin.site.register(TypeResto)
admin.site.register(Commentaire)
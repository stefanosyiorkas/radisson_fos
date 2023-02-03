from django.contrib import admin
from .models import *

class RestaurantAdmin(admin.ModelAdmin):
    pass

class AllergensAdmin(admin.ModelAdmin):
    list_display = ('id', 'allergen_name',)
    ordering = ('id',)


admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Allergens, AllergensAdmin)

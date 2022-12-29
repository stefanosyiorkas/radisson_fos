from django.contrib import admin
from .models import Category, Foods, Allergens, UserOrder, SavedCarts, Table
from tinymce.widgets import TinyMCE
from django.db import models
from django.utils.html import format_html

class CategoryAdmin(admin.ModelAdmin):
    formfield_overrides = {
            models.TextField: {'widget': TinyMCE()},
            }

    ordering = ['category_title_en']

class AllergensAdmin(admin.ModelAdmin):
    list_display = ('id','allergen_name',)
    ordering = ('id',)
class FoodAdmin(admin.ModelAdmin):

    def image_tag(self, obj):
        return format_html('<img style="width: 2.5rem; height: 2.5rem; object-fit: cover;" src="{}" />'.format(obj.dish_image.url))

    image_tag.short_description = 'Image'

    list_display = ('dish_name','dish_description','image_tag','category','price','enabled','hidden')

    list_filter = [
        "category",
    ]

    search_fields = (
        "dish_name",
    )

class TableAdmin(admin.ModelAdmin):
    ordering = ('table_number',)
class MyModelAdmin(admin.ModelAdmin):
    # specify the fields to be displayed in the list view
    list_display = ['dish_name','dish_description','category','price','enabled','hidden']

    # specify the fields to be used as filters in the list view
    list_filter = ['category','enabled','hidden']

    # # specify the fields to be displayed in the form view
    # fields = ['category']

    search_fields = ["dish_name"]

admin.site.register(Category,CategoryAdmin)

admin.site.register(UserOrder)
admin.site.register(SavedCarts)

admin.site.register(Foods, FoodAdmin)
admin.site.register(Allergens, AllergensAdmin)
admin.site.register(Table, TableAdmin)



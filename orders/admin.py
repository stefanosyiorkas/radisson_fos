from django.contrib import admin
from .models import Category, Foods, FoodOption, Drinks, DrinkOption, Allergens, UserOrder, SavedCarts, Table
from django.db import models
from django.utils.html import format_html
from django.contrib.admin.options import StackedInline
from django.shortcuts import HttpResponseRedirect


class CategoryAdmin(admin.ModelAdmin):
    ordering = ['category_title_en']


class AllergensAdmin(admin.ModelAdmin):
    list_display = ('id', 'allergen_name',)
    ordering = ('id',)


class FoodOptionInline(StackedInline):
    model = FoodOption


class FoodAdmin(admin.ModelAdmin):

    def image_tag(self, obj):
        return format_html(
            '<img style="width: 2.5rem; height: 2.5rem; object-fit: cover;" src="{}" />'.format(obj.dish_image.url))

    image_tag.short_description = 'Image'

    list_display = ('dish_name', 'image_tag', 'category', 'price', 'enabled', 'hidden')

    list_filter = [
        "category",
    ]

    search_fields = (
        "dish_name",
    )

    inlines = [FoodOptionInline]

    def response_add(self, request, obj, post_url_continue=None):
        # Save the form
        obj.save()
        last_saved_id = obj.id
        return HttpResponseRedirect(str(request.path + f"{last_saved_id}/change/").replace("add/", ""))


class DrinkOptionInline(StackedInline):
    model = DrinkOption


class DrinksAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'image_tag', 'available')
    inlines = [DrinkOptionInline]

    def image_tag(self, obj):
        return format_html(
            '<img style="width: 2.5rem; height: 2.5rem; object-fit: cover;" src="{}" />'.format(obj.image.url))

    image_tag.short_description = 'Image'

    def response_add(self, request, obj, post_url_continue=None):
        # Save the form
        obj.save()
        last_saved_id = obj.id
        return HttpResponseRedirect(str(request.path + f"{last_saved_id}/change/").replace("add/", ""))


class TableAdmin(admin.ModelAdmin):
    ordering = ('table_number',)


admin.site.register(Category, CategoryAdmin)

admin.site.register(UserOrder)
admin.site.register(SavedCarts)

admin.site.register(Foods, FoodAdmin)
admin.site.register(Drinks, DrinksAdmin)

admin.site.register(Allergens, AllergensAdmin)
admin.site.register(Table, TableAdmin)

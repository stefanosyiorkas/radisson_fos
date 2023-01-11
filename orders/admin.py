from django.contrib import admin
from .models import Category, Foods, FoodOption, Drinks, DrinkOption, Allergens, UserOrder, SavedCarts, Table
from django.contrib import messages
from django.utils.html import format_html
from django.contrib.admin.options import StackedInline
from django.shortcuts import HttpResponseRedirect
from translate import Translator
from .forms import FoodsForm

translator= Translator(to_lang="Greek")
class CategoryAdmin(admin.ModelAdmin):
    ordering = ['order']
    list_display = ['category_title_en','category_title_el','order']

    def response_add(self, request, obj, post_url_continue=None):
        try:
            obj.category_title_en = obj.category_title_en.title()
            obj.category_title_el = translator.translate(obj.category_title_en)
        except Exception as e:
            obj.category_title_en = obj.category_title_en.title()
            obj.category_title_el = ''
            messages.error(request, "Translation failed, please enter manually")

        # Save the form
        obj.save()
        last_saved_id = obj.id
        return HttpResponseRedirect(str(request.path + f"{last_saved_id}/change/").replace("add/", ""))

    def get_form(self, request, obj=None, **kwargs):
        form = super(CategoryAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['category_title_en'].required = True
        form.base_fields['category_title_en'].label = 'Category Title'
        form.base_fields['category_title_el'].label = 'Τίτλος Κατηγορίας'
        form.base_fields['category_title_el'].widget.attrs['placeholder'] = 'This field will be translated to Greek'
        return form


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
    form = FoodsForm

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

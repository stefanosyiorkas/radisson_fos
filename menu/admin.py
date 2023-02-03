from django.contrib import admin
from .models import *
from django.contrib import messages
from django.utils.html import format_html
from django.contrib.admin.options import StackedInline
from django.shortcuts import HttpResponseRedirect
from translate import Translator
from .forms import *
from django.forms import ClearableFileInput
from django.db import models

def image_tag_admin(object):
    try:
        if object.image.url == '/media/none':
            return format_html(
                '<img style="width: 2.5rem; height: 2.5rem; object-fit: cover;" src="/media/media/no-img-available.png" />')
        return format_html(
            '<img style="width: 2.5rem; height: 2.5rem; object-fit: cover;" src="{}" />'.format(object.image.url))
    except ValueError as e:
        logging.error(e)
        return format_html(
            '<img style="width: 2.5rem; height: 2.5rem; object-fit: cover;" src="/media/media/no-img-available.png" />')

translator= Translator(to_lang="Greek")
class CategoryAdmin(admin.ModelAdmin):
    ordering = ['order']
    list_display = ['title_en','title_el','order']

    def response_add(self, request, obj, post_url_continue=None):
        try:
            obj.title_en = obj.title_en.title()
            obj.title_el = translator.translate(obj.title_en)
        except Exception as e:
            obj.title_en = obj.title_en.title()
            obj.title_el = ''
            messages.error(request, "Translation failed, please enter manually")

        # Save the form
        obj.save()
        last_saved_id = obj.id
        return HttpResponseRedirect(str(request.path + f"{last_saved_id}/change/").replace("add/", ""))

    def get_form(self, request, obj=None, **kwargs):
        form = super(CategoryAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['title_en'].required = True
        form.base_fields['title_en'].label = 'Category Title'
        form.base_fields['title_el'].label = 'Τίτλος Κατηγορίας'
        form.base_fields['title_el'].widget.attrs['placeholder'] = 'This field will be translated to Greek'
        return form

class FoodOptionInline(StackedInline):
    model = FoodOption


class FoodAdmin(admin.ModelAdmin):

    def image_tag(self, obj):
        return image_tag_admin(obj)
    image_tag.short_description = 'Image'

    list_display = ('dish_name', 'image_tag', 'category', 'price', 'enabled', 'available')
    list_filter = ["category",]
    search_fields = ("dish_name",)

    inlines = [FoodOptionInline]
    form = FoodsForm

    fields = (
        'category','dish_name','dish_description',
        'image','food_image', 'allergies', 'price',
        'enabled', 'available', 'has_options', 'created_at',
        'updated_at',
    )
    formfield_overrides = {
        models.ImageField: {'widget': ClearableFileInput(attrs={'style': 'display:none;'})},
    }
    readonly_fields = ('food_image','created_at', 'updated_at')

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

    form = DrinksForm

    def image_tag(self, obj):
        return image_tag_admin(obj)
    image_tag.short_description = 'Image'

    def response_add(self, request, obj, post_url_continue=None):
        # Save the form
        obj.save()
        last_saved_id = obj.id
        return HttpResponseRedirect(str(request.path + f"{last_saved_id}/change/").replace("add/", ""))

class UserOrderAdmin(admin.ModelAdmin):
    change_form_template = 'admin/menu/user_order_form.html'
    def has_change_permission(self, request, obj=None):
        return False


class TableAdmin(admin.ModelAdmin):
    ordering = ('table_number',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Subcategory)

admin.site.register(UserOrder, UserOrderAdmin)
admin.site.register(SavedCarts)

admin.site.register(Foods, FoodAdmin)
admin.site.register(Drinks, DrinksAdmin)

admin.site.register(Table, TableAdmin)

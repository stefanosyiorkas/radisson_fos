import logging

from django.contrib import admin
from .forms import *
from .models import *

class RestaurantAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return ['url']
        return ['name', 'url']

    actions = ['delete_model']

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        if 'delete_model' in actions:
            del actions['delete_model']
        return actions

    def delete_model(self, request, obj):
        logging.info(f'>> Deleting model {obj}')

        try:
            with open('core/urls.py', 'r') as fr:
                lines = fr.readlines()

            with open('core/urls.py', 'w') as fw:
                for line in lines:

                    if line.strip('\n') != f'urlpatterns+=[path("{obj.url}/", include("{obj.url.replace("_menu", "_app")}.urls"))]':
                        fw.write(line)
            logging.info(">> URLs Deleted")

            with open('core/restaurant_apps.py', 'r') as fr:
                lines = fr.readlines()

            with open('core/restaurant_apps.py', 'w') as fw:
                for line in lines:

                    if line.strip('\n') != f'NEW_APPS+=["{obj.url.replace("_menu", "_app")}.apps.MenuConfig"]':
                        fw.write(line)
            logging.info(">> App Configuration Deleted")
        except Exception as e:
            logging.error(str(e))

        try:
            shutil.rmtree(obj.url.replace('_menu', '_app'))
            logging.info(">> App Files Deleted")
        except Exception as e:
            logging.error(str(e))

        try:
            obj.delete()
            logging.info(">> Object Deleted")
        except Exception as e:
            logging.error(str(e))

        logging.info('>> Model Deleted')

class AllergensAdmin(admin.ModelAdmin):
    list_display = ('id', 'allergen_name',)
    ordering = ('id',)


admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Allergens, AllergensAdmin)

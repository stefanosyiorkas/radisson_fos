import logging
import os
import shutil
from django.db import models


class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    opens_at = models.TimeField(null=True, blank=True)
    closes_at = models.TimeField(null=True, blank=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    logo = models.ImageField(upload_to='logos', blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):

        self.name = self.name.title()
        new_app_name = self.name.lower().replace(' ', '')
        self.url = new_app_name + "_menu"
        new_app_name += "_app"

        if not os.path.exists(new_app_name):
            try:
                logging.info(">> Copying app files")
                shutil.copytree('menu/', new_app_name)

                logging.info(">> Registering app")
                restaurants_file = open('core/restaurant_apps.py', 'a')
                restaurants_file.write(f'NEW_APPS+=["{new_app_name}.apps.MenuConfig"]\n')
                restaurants_file.close()

                logging.info(">> Creating URLs")
                core_urls = open('core/urls.py', 'a')
                core_urls.write(f'urlpatterns+=[path("{self.url}/", include("{new_app_name}.urls"))]\n')
                core_urls.close()

                logging.info(">> Migrating to main")
                os.system('python manage.py makemigrations && python manage.py migrate')

                logging.info(">> App created")
            except Exception as e:
                logging.error(">> Error creating app")
                logging.error(str(e))

        super().save(*args, **kwargs)


class Allergens(models.Model):
    allergen_name = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Allergen"
        verbose_name_plural = "Allergens"

    def __str__(self):
        return f"{self.allergen_name}"

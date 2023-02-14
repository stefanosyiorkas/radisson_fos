import os
from django.apps import AppConfig

class MenuConfig(AppConfig):
    name = os.path.dirname(os.path.realpath(__file__)).split('/')[-1]
    ordering = False
    restaurant = os.path.dirname(os.path.realpath(__file__)).split('/')[-1].replace('_app', '')

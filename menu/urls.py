from . import views
from .apps import MenuConfig as Configuration
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = Configuration.name

urlpatterns = [
    path("", views.index, name="index"),
    path("contact", views.contact, name="contact"),
    path("set_default_image/<str:category>", views.set_default_image,  name="set_default_image"),
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

if Configuration.ordering:
    from .ordering_functionality.ordering_urls import orders_urlpatterns
    urlpatterns += orders_urlpatterns

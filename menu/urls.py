from . import views
from .apps import MenuConfig as Configuration
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = "menu"

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_request, name="login"),
    path("register", views.register, name="register"),
    path("logout", views.logout_request, name="logout"),
    path("contact", views.contact, name="contact"),
    path("set_default_image", views.set_default_image,  name="set_default_image"),
    path("check_superuser", views.check_superuser, name="check_superuser"),
    path("check_staff_user", views.check_staff_user, name="check_staff_user"),
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

if Configuration.ordering:
    from menu.ordering_functionality.ordering_urls import orders_urlpatterns
    urlpatterns += orders_urlpatterns

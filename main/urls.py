from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = "main"

urlpatterns = [
    path("", views.landing, name="landing"),
    path("login/", views.login_request, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout_request, name="logout"),
    path("check_superuser", views.check_superuser, name="check_superuser"),
    path("check_staff_user", views.check_staff_user, name="check_staff_user"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

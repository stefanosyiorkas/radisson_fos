from django.contrib import admin
from django.urls import include, path, re_path

urlpatterns = [
    path("", include("main.urls")),
    path("admin/", admin.site.urls),
    re_path(r'^i18n/', include('django.conf.urls.i18n')),
]
handler404='main.views.handle_404'
handler500='main.views.handle_500'
handler403='main.views.handle_403'

urlpatterns+=[path("therestaurant_menu/", include("therestaurant_app.urls"))]
urlpatterns+=[path("alldaylounge_menu/", include("alldaylounge_app.urls"))]

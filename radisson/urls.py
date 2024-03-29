"""
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path


urlpatterns = [
    path("", include("orders.urls")),
    path("admin/", admin.site.urls),
    path('tinymce/', include('tinymce.urls')),
    path("convert/", include("guest_user.urls")),
    re_path(r'^i18n/', include('django.conf.urls.i18n')),
]
handler404='orders.views.handle_404'
handler500='orders.views.handle_500'
handler403='orders.views.handle_403'
#
# admin.site.site_header = "Admin Dashboard"
# admin.site.site_title = "Radisson FOS Admin Dashboard"
# admin.site.index_title = "Radisson FOS Admin Dashboard"

from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "orders"

urlpatterns = [
    path("", views.index, name="index"),
    path("guest", views.hello_guest, name="guest"),
    path("login", views.login_request, name="login"),
    path("register/", views.register, name="register"),
    path("logout", views.logout_request, name="logout"),
    path("contact", views.contact, name="contact"),
    path("cart", views.cart, name="cart"),
    path("checkout", views.checkout, name="checkout"),
    path("view-orders", views.view_orders, name="view_orders"),
    path("update-orders", views.update_orders, name="update_orders"),
    path("mark_order_as_delivered", views.mark_order_as_delivered, name="mark_order_as_delivered"),
    path("mark_order_as_pending", views.mark_order_as_pending, name="mark_order_as_pending"),
    path("set_default_image", views.set_default_image,  name="set_default_image"),
    path("save_cart", views.save_cart, name="save_cart"),
    path("retrieve_saved_cart", views.retrieve_saved_cart, name="retrieve_saved_cart"),
    path("check_superuser", views.check_superuser, name="check_superuser"),
    path("check_staff_user", views.check_staff_user, name="check_staff_user"),
    path("order_success", views.order_success, name="order_success"),
    path("order-approved", views.order_approved, name="order_approved")

]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

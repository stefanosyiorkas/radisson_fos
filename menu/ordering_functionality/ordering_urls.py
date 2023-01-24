from django.urls import include, path
from menu import views

orders_urlpatterns = [
    path("guest", views.hello_guest, name="guest"),
    path("cart", views.cart, name="cart"),
    path("checkout", views.checkout, name="checkout"),
    path("view-orders", views.view_orders, name="view_orders"),
    path("update-orders", views.update_orders, name="update_orders"),
    path("mark_order_as_delivered", views.mark_order_as_delivered, name="mark_order_as_delivered"),
    path("mark_order_as_pending", views.mark_order_as_pending, name="mark_order_as_pending"),
    path("save_cart", views.save_cart, name="save_cart"),
    path("retrieve_saved_cart", views.retrieve_saved_cart, name="retrieve_saved_cart"),
    path("order_success", views.order_success, name="order_success"),
    path("order-approved", views.order_approved, name="order_approved"),
    path("convert/", include("guest_user.urls")),
]

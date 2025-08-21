from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("products/", views.product_list, name="product_list"),
    path("add-to-cart/", views.add_to_cart, name="add_to_cart"),
    path("remove-from-cart/", views.remove_from_cart, name="remove_from_cart"),
    path("cart/", views.cart_view, name="cart"),
    path('update-cart', views.update_cart_item, name='update_cart_item'),
    path('checkout/', views.make_order ,name='checkout'),
    path("makepayent/", views.make_payment, name="make_payment"),
    path("orders/", views.orders_view, name="orders"),
    
]
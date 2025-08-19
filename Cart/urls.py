# shop/urls.py
from django.urls import path
from .views import CartView, AddToCartView, UpdateCartItemView, DeleteCartItemView

urlpatterns = [
    path("cart/", CartView.as_view(), name="cart"),
    path("cart/add/", AddToCartView.as_view(), name="add-to-cart"),
    path("cart/item/<int:item_id>/update/", UpdateCartItemView.as_view(), name="update-cart-item"),
    path("cart/item/<int:item_id>/remove/", DeleteCartItemView.as_view(), name="remove-cart-item"),
]

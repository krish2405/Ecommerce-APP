from django.urls import path
from .views import OrderListCreateView, MockPaymentView,ActiveOrderView

urlpatterns = [
    path("orders/", OrderListCreateView.as_view(), name="order-list-create"),
    path("orders/active/", ActiveOrderView.as_view(), name="pendingorders"),
    path("orders/<int:pk>/pay/", MockPaymentView.as_view(), name="order-payment"),
]

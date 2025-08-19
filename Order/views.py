from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from Order.tasks import send_order_confirmation_email

from .models import Order, OrderItem
from .serializers import OrderSerializer
from Cart.models import Cart


class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user,status="PENDING")

    def post(self, request, *args, **kwargs):
        user = request.user
        cart = Cart.objects.filter(user=user).first()

        if not cart or cart.items.count() == 0:
            return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            order = Order.objects.create(user=user, total_price=0)
            total = 0

            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price,
                )
                total += item.product.price * item.quantity

            order.total_price = total
            order.save()
            send_order_confirmation_email.delay(order.id, user.email)

            # Clear the cart
            cart.items.all().delete()

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


class MockPaymentView(generics.UpdateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()

    def put(self, request, pk=None):
        try:
            order = Order.objects.get(pk=pk, user=request.user)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        # Fake payment logic
        payment_status = request.data.get("status", "FAILED")
        if payment_status == "PAID":
            order.status = "PAID"
        else:
            order.status = "FAILED"
        order.save()

        return Response(OrderSerializer(order).data)
    
class ActiveOrderView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Order.objects.filter(user=self.request.user, status="PENDING").last()


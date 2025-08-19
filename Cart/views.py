from django.shortcuts import render
from rest_framework.response import Response
from .models import Cart,CartItems
from Shop.models import Product
from .serializers import CartSerializer, CartItemsSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, permissions


class CartView(generics.RetrieveAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=CartSerializer

    def get_object(self):
        cart,_=Cart.objects.get_or_create(user=self.request.user)
        return cart
    

class AddToCartView(generics.CreateAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=CartItemsSerializer

    def create(self, request, *args, **kwargs):
        cart,_=Cart.objects.get_or_create(user=self.request.user)
        product_id=request.data.get('product_id')
        quantity=request.data.get('quantity', 1)

        try:
            product=Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=404) 
        
        cart_item,created=CartItems.objects.get_or_create(cart=cart, product=product)
        cart_item.quantity += quantity if not created else quantity
        cart_item.save()

        return Response(CartItemsSerializer(cart_item).data, status=201 if created else 200)
        
class UpdateCartItemView(generics.UpdateAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=CartItemsSerializer
    lookup_url_kwarg='item_id'

    def get_queryset(self):
        return CartItems.objects.filter(cart__user=self.request.user)
    
class DeleteCartItemView(generics.DestroyAPIView):
    permission_classes=[IsAuthenticated]
    lookup_url_kwarg='item_id'

    def get_queryset(self):
        return CartItems.objects.filter(cart__user=self.request.user)

    def perform_destroy(self, instance):
        instance.delete()
        return Response(status=204)

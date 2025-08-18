from django.shortcuts import render
from rest_framework import generics,permissions
from .models import Category,Product
from .serializer import ProductSerializer,CategorySeralizer


class CategoryListCreateAV(generics.ListCreateAPIView):
    queryset=Category.objects.all()
    serializer_class=CategorySeralizer
    permission_classes=[permissions.IsAdminUser]


class CategoryDetailAV(generics.RetrieveUpdateDestroyAPIView):
    queryset=Category.objects.all()
    serializer_class=CategorySeralizer
    permission_classes=[permissions.IsAdminUser]

class ProductListAV(generics.ListCreateAPIView):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    def get_permissions(self):
        if self.request.method =='POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]
    

class ProductDetailAv(generics.RetrieveUpdateDestroyAPIView):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]
    
    def perform_update(self, serializer):
        if self.request.user==self.get_object().created_by or self.request.user.is_staff:
            serializer.save()
        else:
            raise permissions.PermissionDenied("You do not have permission to update this product.")
        

    def perform_destroy(self, instance):
        if self.request.user == instance.created_by or self.request.user.is_staff:
            instance.delete()
        else:
            raise permissions.PermissionDenied("You cannot delete this product.")
from django.urls import path
from .views import ProductDetailAv,ProductListAV,CategoryListCreateAV,CategoryDetailAV


urlpatterns = [
    path('categories/',CategoryListCreateAV.as_view(),name='categories')
    ,path('categories/<int:pk>/',CategoryDetailAV.as_view(),name='category-detail'),
    path('products/',ProductListAV.as_view(),name="product"),
    path('products/<int:pk>/',ProductDetailAv.as_view(),name="product-detail")
]

from django.db import models
from django.contrib.auth.models import User
from Shop.models import Product 

# Create your models here.
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    def __str__(self):
        return f"Cart of {self.user.username}"
    
class CartItems(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='items')
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='cart_items')
    quantity=models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} * {self.quantity}"



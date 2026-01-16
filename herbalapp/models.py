from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    desc= models.TextField(max_length=500)
    phonenumber = models.IntegerField()
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Product(models.Model):
    product_name = models.CharField(max_length=255)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, blank=True)
    subcategory = models.CharField(max_length=255, default="")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    desc = models.TextField(max_length=500)
    product_image = models.ImageField(upload_to='images', default='images/placeholder.png')
    size = models.CharField(max_length=50, default="")      
    plant_type = models.CharField(max_length=50, default="") 
    thc = models.CharField(max_length=50, default="")        
    cbd = models.CharField(max_length=50, default="")       
    effects = models.CharField(max_length=200, default="")  
    tags = models.CharField(max_length=100, default="")     
    sku = models.CharField(max_length=50, default="")      
    def __str__(self):
        return self.product_name
from django.conf import settings

# ✅ ONLY ONE CART MODEL
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.product.price * self.quantity
# ORDER MODELS

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.product.product_name







    
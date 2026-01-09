from django.db import models

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

    def __str__(self):
        return self.product_name






    
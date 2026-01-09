from django.contrib import admin
from herbalapp.models import Contact
from herbalapp.models import Product,Category

# Register your models here.
admin.site.register(Contact)
admin.site.register(Product)
admin.site.register(Category)
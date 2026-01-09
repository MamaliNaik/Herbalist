from django.shortcuts import render, redirect
from herbalapp.models import Product, Contact

# Create your views here.
def home(request):
    return render(request, 'home.html')

def product_detail(request, id):
    product = Product.objects.get(id=id)
    return render(request, 'product_detail.html', {'product': product})


# Shop view with category filter

def product_list(request):
    category_name = request.GET.get('category')

    if category_name:
        products = Product.objects.filter(
            category__name__iexact=category_name
        )
    else:
        products = Product.objects.all()

    context = {
        'products': products,
        'selected_category': category_name
    }

    return render(request, 'product.html', context)
# Contact view

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        phone = request.POST.get('phone')
        myquery = Contact(name=name, email=email, desc=message, phonenumber=phone)
        myquery.save()
    return render(request, 'contact.html')
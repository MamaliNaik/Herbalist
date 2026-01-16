from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Cart, CartItem, Order, OrderItem, Contact


def home(request):
    return render(request, 'home.html')


def product_list(request):
    category_name = request.GET.get('category')

    if category_name:
        products = Product.objects.filter(category__name__iexact=category_name)
    else:
        products = Product.objects.all()

    return render(request, 'product.html', {'products': products})


@login_required(login_url='login')
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'product_detail.html', {'product': product})


@login_required(login_url='login')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        cart_item.quantity += 1

    cart_item.save()
    return redirect('cart')


@login_required(login_url='login')
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()

    total = sum(item.total_price() for item in items)

    return render(request, 'cart.html', {
        'items': items,
        'total': total
    })


@login_required(login_url='login')
def update_cart(request, item_id, action):
    item = get_object_or_404(CartItem, id=item_id)

    if action == 'inc':
        item.quantity += 1
    elif action == 'dec':
        item.quantity -= 1
        if item.quantity == 0:
            item.delete()
            return redirect('cart')

    item.save()
    return redirect('cart')
@login_required(login_url='login')
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    items = cart.items.all()

    if not items.exists():
        return redirect('cart')

    total = sum(item.total_price() for item in items)

    if request.method == 'POST':
        order = Order.objects.create(
            user=request.user,
            total_amount=total,
            is_paid=True  # later you can integrate payment
        )

        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        # clear cart
        items.delete()

        return redirect('order_success')

    return render(request, 'checkout.html', {
        'items': items,
        'total': total
    })
@login_required(login_url='login')
def order_success(request):
    return render(request, 'order_success.html')


def contact(request):
    if request.method == 'POST':
        Contact.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            desc=request.POST.get('message'),
            phonenumber=request.POST.get('phone')
        )
    return render(request, 'contact.html')



@login_required(login_url='login')
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'order_history.html', {'orders': orders})
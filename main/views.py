from django.shortcuts import render, get_object_or_404, redirect
from .models import Fruit


def index(request):
    fruits = Fruit.objects.all()
    return render(request, 'index.html', {'fruits': fruits})


def shop(request):
    fruits = Fruit.objects.all()
    return render(request, 'shop.html', {'fruits': fruits})


def shop_detail(request):
    return render(request, 'shop-detail.html')


def cart(request):
    cart_session = request.session.get('cart', {})
    cart_items = []

    for fruit_id, quantity in cart_session.items():
        fruit = get_object_or_404(Fruit, id=fruit_id)
        cart_items.append({
            'fruit': fruit,
            'quantity': quantity,
        })

    context = {
        'cart_items': cart_items,
    }
    return render(request, 'cart.html', context)


def add_to_cart(request, fruit_id):
    cart_session = request.session.get('cart', {})
    fruit_id_str = str(fruit_id)

    if fruit_id_str in cart_session:
        cart_session[fruit_id_str] += 1
    else:
        cart_session[fruit_id_str] = 1

    request.session['cart'] = cart_session
    return redirect(request.META.get('HTTP_REFERER', 'index'))


def checkout(request):
    return render(request, 'checkout.html')


def testimonial(request):
    return render(request, 'testimonial.html')


def contact(request):
    return render(request, 'contact.html')
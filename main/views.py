import re
from decimal import Decimal, InvalidOperation

from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from .models import Fruit

SHIPPING = Decimal('3.00')


def parse_price(value):
    """'4.99', '4.99 $', '$4,99' -> Decimal('4.99')"""
    cleaned = re.sub(r'[^\d.,]', '', str(value)).replace(',', '.')
    try:
        return Decimal(cleaned)
    except InvalidOperation:
        return Decimal('0')


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
    subtotal = Decimal('0')

    for fruit_id, quantity in cart_session.items():
        fruit = Fruit.objects.filter(id=fruit_id).first()
        if fruit is None:
            continue
        price = parse_price(fruit.price)
        total = price * quantity
        subtotal += total
        cart_items.append({
            'fruit': fruit,
            'quantity': quantity,
            'price': price,
            'total': total,
        })

    shipping = SHIPPING if cart_items else Decimal('0')
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping': shipping,
        'total': subtotal + shipping,
    })


@require_POST
def add_to_cart(request, fruit_id):
    cart_session = request.session.get('cart', {})
    key = str(fruit_id)
    cart_session[key] = cart_session.get(key, 0) + 1
    request.session['cart'] = cart_session
    return redirect(request.META.get('HTTP_REFERER') or 'shop')


@require_POST
def update_cart(request, fruit_id, action):
    cart_session = request.session.get('cart', {})
    key = str(fruit_id)
    if key in cart_session:
        if action == 'inc':
            cart_session[key] += 1
        elif action == 'dec':
            cart_session[key] -= 1
        if cart_session[key] <= 0:
            del cart_session[key]
    request.session['cart'] = cart_session
    return redirect('cart')


@require_POST
def remove_from_cart(request, fruit_id):
    cart_session = request.session.get('cart', {})
    cart_session.pop(str(fruit_id), None)
    request.session['cart'] = cart_session
    return redirect('cart')


def checkout(request):
    return render(request, 'checkout.html')


def testimonial(request):
    return render(request, 'testimonial.html')


def contact(request):
    return render(request, 'contact.html')
import re
from decimal import Decimal, InvalidOperation

from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .forms import OrderForm
from .models import Fruit, Order, OrderItem

SHIPPING = Decimal('3.00')


def parse_price(value):
    """'4.99', '4.99 $', '$4,99' -> Decimal('4.99')"""
    cleaned = re.sub(r'[^\d.,]', '', str(value)).replace(',', '.')
    try:
        return Decimal(cleaned)
    except InvalidOperation:
        return Decimal('0')


def build_cart(request):
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
    return {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping': shipping,
        'total': subtotal + shipping,
    }


def index(request):
    return render(request, 'index.html', {'fruits': Fruit.objects.all()})


def shop(request):
    query = request.GET.get('q', '').strip()
    fruits = Fruit.objects.all()
    if query:
        fruits = fruits.filter(title__icontains=query)
    return render(request, 'shop.html', {'fruits': fruits, 'query': query})


def fruit_detail(request, fruit_id):
    fruit = get_object_or_404(Fruit, id=fruit_id)
    related = Fruit.objects.exclude(id=fruit.id)[:4]
    return render(request, 'shop-detail.html', {
        'fruit': fruit,
        'price': parse_price(fruit.price),
        'related': related,
    })


def cart(request):
    return render(request, 'cart.html', build_cart(request))


@require_POST
def add_to_cart(request, fruit_id):
    fruit = get_object_or_404(Fruit, id=fruit_id)
    try:
        quantity = max(1, min(int(request.POST.get('quantity', 1)), 99))
    except ValueError:
        quantity = 1

    cart_session = request.session.get('cart', {})
    key = str(fruit.id)
    cart_session[key] = cart_session.get(key, 0) + quantity
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
    data = build_cart(request)

    if request.method == 'POST' and data['cart_items']:
        form = OrderForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                order = form.save(commit=False)
                order.total = data['total']
                order.save()
                for item in data['cart_items']:
                    OrderItem.objects.create(
                        order=order,
                        fruit=item['fruit'],
                        title=item['fruit'].title,
                        price=item['price'],
                        quantity=item['quantity'],
                    )
            request.session['cart'] = {}
            request.session['last_order_id'] = order.id
            return redirect('order_success')
    else:
        form = OrderForm()

    data['form'] = form
    return render(request, 'checkout.html', data)


def order_success(request):
    order_id = request.session.get('last_order_id')
    if not order_id:
        return redirect('index')
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order_success.html', {'order': order})


def testimonial(request):
    return render(request, 'testimonial.html')


def contact(request):
    return render(request, 'contact.html')
from django.db import models

class Fruit(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/', verbose_name='Image')
    description = models.TextField(verbose_name='Description')
    price = models.CharField(verbose_name='Price', max_length=100)

    class Meta:
        verbose_name = 'Fruit'
        verbose_name_plural = 'Fruits'

def add_to_cart(request, fruit_id):
    # Получаем корзину из сессии или создаем пустую, если её нет
    cart = request.session.get('cart', {})

    fruit_id_str = str(fruit_id)

    # Если товар уже есть в корзине, увеличиваем количество на 1, иначе добавляем
    if fruit_id_str in cart:
        cart[fruit_id_str] += 1
    else:
        cart[fruit_id_str] = 1

    # Сохраняем корзину обратно в сессию
    request.session['cart'] = cart

    # Возвращаем пользователя туда, откуда он нажал кнопку
    return redirect(request.META.get('HTTP_REFERER', 'home'))


def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []

    for fruit_id, quantity in cart.items():
        fruit = get_object_or_404(Fruit, id=fruit_id)
        cart_items.append({
            'fruit': fruit,
            'quantity': quantity,
        })

    context = {
        'cart_items': cart_items,
    }
    return render(request, 'cart.html', context)
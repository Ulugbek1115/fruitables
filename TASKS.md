# Fruitables — nimalarni to'g'irlash kerak

Loyiha ishga tushyapti, lekin bir nechta sahifa xato beradi, savat esa ishlamaydi. Pastda hammasini yozib qo'ydim.
Tartib bilan, birinchi punktdan boshlab qil. Har bir qismdan keyin `python manage.py runserver` qilib tekshirib tur.

Eslatma: `base.html` ni qayta qildim. Endi unda faqat menyu, footer va `{% block content %}` bor.
Bosh sahifadagi bloklar (hero, mahsulotlar, fikrlar) `index.html` ga o'tdi. `index.html` ni `main/templates/` dan
`templates/` ga ko'chirdim.

---

## 1-qism. Xatolarni to'g'irlash

**1. `{% url '404' %}` xato beradi**
`checkout.html` (85-qator), `testimonial.html` (78-qator), `404.html` (77-qator) da `{% url '404' %}` bor,
lekin `404` degan url yo'q. Shu sababli checkout va testimonial sahifalari 500 xato beradi.
`404.html` ham buzilgan, shuning uchun `DEBUG = False` bo'lsa har qanday 404 xato 500 ga aylanadi.
Bu linklarni `href="#"` qil yoki o'chir.

**2. Rasmlar chiqmaydi**
`settings.py` da `MEDIA_URL` va `MEDIA_ROOT` yo'q. Shuning uchun admin orqali yuklangan rasmlar
loyiha ichidagi `images/` papkaga tushyapti va saytda ko'rinmayapti. Shuni qo'sh:
```python
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'
```
`config/urls.py` ga media fayllarni ulab qo'y (`static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)`).
Keyin `images/` papkani o'chir, rasmlarni admin orqali qaytadan yukla.

**3. `add_to_cart` da tekshiruv yo'q**
`cart/add/999/` qilsa, yo'q mahsulot savatga tushadi, keyin `cart/` sahifasi doim 404 beradi.
`add_to_cart` boshida `get_object_or_404(Fruit, id=fruit_id)` qil.

**4. `models.py` da ortiqcha kod**
`models.py` ichida `add_to_cart` va `cart_view` funksiyalari qolib ketgan. Ular `views.py` da bor.
`models.py` dan o'chir — modelda faqat model bo'lishi kerak.

---

## 2-qism. Savatni ishlatish

**5. `Fruit` modeli**
- `price` ni `CharField` emas, `DecimalField(max_digits=10, decimal_places=2)` qil. Matn bilan summani hisoblab bo'lmaydi.
- `__str__` qo'sh, admin panelda "Fruit object (1)" emas, nomi ko'rinsin.
- Keyin `makemigrations` va `migrate` qil.

**6. `cart` view**
Har bir mahsulot uchun `fruit.price * quantity` ni hisobla, umumiy summani ham hisobla.
`context` ga `item_total` va `total` ni qo'sh.

**7. `cart.html`**
- Tepasiga `{% extends 'base.html' %}` yoz, menyu va footerni o'chir, qolganini `{% block content %}` ichiga ol.
- Jadvaldagi 3 ta qotirib yozilgan `<tr>` (Big Banana 2.99 $) ni o'chir, o'rniga
  `{% for item in cart_items %}` ... `{% empty %}` ... `{% endfor %}` qil.
- Pastdagi Subtotal va Total ga `{{ total }}` ni chiqar.

**8. Savatdan o'chirish**
`remove_from_cart` view yoz (`cart_session.pop(str(fruit_id), None)`) va url qo'sh: `cart/remove/<int:fruit_id>/`.
`cart.html` dagi ✕ tugmasini shu urlga ula.

---

## 3-qism. Qolgan sahifalar

**9. `shop.html`**
View `fruits` ni yuboryapti, lekin shablonda ishlatilmagan, mahsulotlar qotirib yozilgan.
`{% for fruit in fruits %}` bilan bazadan chiqar.

**10. `shop-detail`**
Hozir `shop-detail/` da id yo'q, aniq bitta mahsulotni ochib bo'lmaydi.
Url ni `shop-detail/<int:pk>/` qil, view da `get_object_or_404(Fruit, pk=pk)` qil, shablonda chiqar.
Mahsulot kartochkalaridagi linklarni `{% url 'shop_detail' fruit.pk %}` qil.

**11. Hamma shablonlar `base.html` dan foydalansin**
`shop`, `shop-detail`, `cart`, `checkout`, `testimonial`, `contact`, `404` — hammasi to'liq sahifa nusxasi.
Har birida `{% extends 'base.html' %}` qil, menyu, footer va skriptlarni o'chir,
faqat o'rtadagi qismni `{% block content %}` ichida qoldir.

---

## 4-qism. Kodni tozalash

**12.** `config/urls.py` dagi `contact` ni `main/urls.py` ga o'tkaz, `from main import views` ni o'chir.

**13.** `admin.py` da `User` import qilingan, lekin ishlatilmagan — o'chir. `from .models import *` emas, `from .models import Fruit` yoz.

**14.** `templates/Module_1.py` — bo'sh fayl, o'chir.

**15.** `locale/ru/LC_MESSAGES/django.po` da "100% xavfsiz to'lov tizimi" tarjima qilinmagan. Tarjima qil, `compilemessages` qil.

---

## 5-qism. Qo'shimcha

**16. `static/lib/` papka yo'q**
`.gitignore` dagi `lib/` qatori `static/lib/` ni ham e'tiborsiz qoldiryapti, shuning uchun lightbox, owlcarousel,
easing va waypoints repozitoriyaga tushmagan. Saytda ular 404 beradi, karusel ishlamaydi.
`.gitignore` da `lib/` ni `/lib/` ga o'zgartir, `static/lib/` ni qo'shib commit qil.

**17. Til almashtirgich ishlamaydi**
`/ru/shop/` sahifasida EN tanlansa, yana `/ru/shop/` ga qaytadi.
`base.html` dagi `next` maydoniga `request.path` ni til prefiksisiz (`/ru/` siz) yubor.

**18. Loyihani ishga tushirish**
Endi `requirements.txt` bor:
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py compilemessages
```
`.mo` fayllar endi git'da saqlanmaydi, shuning uchun `compilemessages` qilish shart.
Buning uchun gettext kerak: `sudo apt install gettext`.

---

Hammasini qilib bo'lgach, menga yoz — tekshirib beraman.

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('shop/', views.shop, name='shop'),
    path('shop-detail/', views.shop_detail, name='shop_detail'),
    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:fruit_id>/', views.add_to_cart, name='add_to_cart'), # <-- Вот эта новая строчка
    path('checkout/', views.checkout, name='checkout'),
    path('testimonial/', views.testimonial, name='testimonial'),
]
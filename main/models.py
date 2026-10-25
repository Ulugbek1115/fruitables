from django.db import models


class Fruit(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/', verbose_name='Image')
    description = models.TextField(verbose_name='Description')
    price = models.CharField(verbose_name='Price', max_length=100)

    class Meta:
        verbose_name = 'Fruit'
        verbose_name_plural = 'Fruits'

    def __str__(self):
        return self.title


class Order(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    company = models.CharField(max_length=150, blank=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postcode = models.CharField(max_length=20)
    phone = models.CharField(max_length=30)
    email = models.EmailField()
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Order #{self.id} - {self.first_name} {self.last_name}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    fruit = models.ForeignKey(Fruit, null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.title} x {self.quantity}'
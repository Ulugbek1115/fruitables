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
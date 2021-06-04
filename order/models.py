from django.db import models
from cart.models import Cart
from django.contrib.auth.models import User

class Order(models.Model):
    cart = models.ManyToManyField(Cart, verbose_name='Товары с корзины')
    price = models.PositiveIntegerField(default=0, verbose_name='Стоимость заказа')
    payment = models.BooleanField(default=0, help_text='0 - онлайн перевод, 1 - наложенный платеж' )
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='ID пользователя')
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    second_name = models.CharField(max_length=50, verbose_name='Фамилия')
    address = models.CharField(max_length=150, verbose_name='Адрес')
    post_type = models.CharField(max_length=50, verbose_name='Тип доставки')
    status = models.CharField(max_length=50, verbose_name='Статус заказа')
    commentary = models.TextField(max_length=500, verbose_name='Комментарии к заказу', blank=True)


    def __str__(self):
        return f'{self.user_id} - {self.id}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


# Create your models here.

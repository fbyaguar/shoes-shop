from django.db import models
from shoes.models import Shoes
from django.contrib.auth.models import User

class Cart(models.Model):
    shoes = models.ForeignKey(Shoes, on_delete=models.CASCADE, verbose_name='ID товара')
    number =models.PositiveSmallIntegerField(default=1,verbose_name='Количество')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='ID пользователя')

    def __str__(self):
        return f'{self.user_id} - {self.shoes}'

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'


# Create your models here.

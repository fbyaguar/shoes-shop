from django.db import models
from shoes.models import Shoes
from django.contrib.auth.models import User


class Wishlist(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='ID пользователя')
    shoes_id = models.ForeignKey(Shoes, on_delete=models.CASCADE, verbose_name='ID товара')
    size = models.PositiveSmallIntegerField(default=0,verbose_name='Размер')

    def __str__(self):
        return f'{self.user_id} - {self.shoes_id}'

    class Meta:
        verbose_name = 'Избранный товар'
        verbose_name_plural = 'Избранные товары'


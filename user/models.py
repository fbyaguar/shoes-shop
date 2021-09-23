from django.db import models
from shoes.models import Shoes
from django.contrib.auth.models import User
# class User(models.Model):
#     login = models.CharField(max_length=50, verbose_name='Логин')
#     first_name = models.CharField(max_length=50, verbose_name='Имя', blank=True)
#     second_name = models.CharField(max_length=50, verbose_name='Фамилия',  blank=True)
#     password = models.CharField(max_length=50, verbose_name='Пароль')
#     email = models.EmailField(verbose_name='Е-мейл',  blank=True)
#     telephone = models.CharField(max_length=50, verbose_name='Номер телефона')
#     address = models.CharField(max_length=50, verbose_name='Адресс',  blank=True)
#     ip = models.CharField(max_length=50, verbose_name='IP пользователя')
#     url = models.SlugField(max_length=150, unique=True)
#
#     def __str__(self):
#         return self.login
#
#     class Meta:
#         verbose_name = 'Пользователь'
#         verbose_name_plural = 'Пользователи'



class Wishlist(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='ID пользователя')
    shoes_id = models.ForeignKey(Shoes, on_delete=models.CASCADE, verbose_name='ID товара')
    size = models.PositiveSmallIntegerField(default=0,verbose_name='Размер')

    def __str__(self):
        return f'{self.user_id} - {self.shoes_id}'

    class Meta:
        verbose_name = 'Избранный товар'
        verbose_name_plural = 'Избранные товары'


# Create your models here.

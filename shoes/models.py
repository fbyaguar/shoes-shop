from django.db import models
from django.urls import reverse


class Category(models.Model):
    title = models.CharField(max_length=150, verbose_name='Наименование')
    url = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Size(models.Model):
    number = models.PositiveSmallIntegerField(default=0,verbose_name='Размер ноги')
    # twenty = models.BooleanField(default=False, verbose_name='20')
    # twenty_one = models.BooleanField(default=False, verbose_name='21')
    # twenty_two = models.BooleanField(default=False, verbose_name='22')
    # twenty_three = models.BooleanField(default=False, verbose_name='23')
    # twenty_four = models.BooleanField(default=False, verbose_name='24')
    # twenty_five= models.BooleanField(default=False, verbose_name='25')
    url = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return str(self.number)

    class Meta:
        verbose_name = 'Размер'
        verbose_name_plural = 'Размеры'


class Season(models.Model):
    title = models.CharField(max_length=150, verbose_name='Наименование')
    url = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Сезон'
        verbose_name_plural = 'Сезоны'


class Brand(models.Model):
    title = models.CharField(max_length=150, verbose_name='Наименование')
    url = models.SlugField(max_length=150, unique=True)
    logo = models.ImageField(upload_to='logo/%Y/%M/%D', blank=True, verbose_name='Логотип')
    content = models.TextField(max_length=1000, blank=True, verbose_name='Описание')

    def __str__(self):
        return self.title


    class Meta:
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'



class Country(models.Model):
    title = models.CharField(max_length=150, verbose_name='Наименование')
    url = models.SlugField(max_length=150, unique=True)
    flag = models.ImageField(upload_to='flag/%Y/%M/%D', blank=True, verbose_name='Флаг')

    def __str__(self):
        return self.title


    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'



class Material(models.Model):
    top = models.CharField(max_length=50, verbose_name='Верх', blank=True)
    sole = models.CharField(max_length=50, verbose_name='Подошва', blank=True)
    strap = models.CharField(max_length=50, verbose_name='Ремешок', blank=True)
    lining = models.CharField(max_length=50, verbose_name='Подкладка', blank=True)

    class Meta:
        verbose_name = 'Материал'
        verbose_name_plural = 'Материалы'




class Shoes(models.Model):
    title = models.CharField(max_length=150, verbose_name='Наименование')
    price = models.PositiveSmallIntegerField(default=0,verbose_name='Цена')
    created = models.DateTimeField(auto_now_add=True,verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True,verbose_name='Дата обновления')
    photo = models.ImageField(upload_to='photos/%Y/%M/%D', blank=True, verbose_name='Фото',help_text='размер фото 200X200 или изменить на другой')
    # short_content = models.TextField(max_length=200, blank=True, verbose_name='Короткое описание')
    content = models.TextField(max_length=1000, blank=True, verbose_name='Описание')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Категория')
    size = models.ManyToManyField(Size, verbose_name='Размеры')
    season = models.ForeignKey(Season,on_delete=models.PROTECT,verbose_name='Сезон')
    sex = models.BooleanField(default=False, help_text='1 - мальчик, 0 - девочка', verbose_name='Пол')
    brand = models.ForeignKey(Brand,on_delete=models.PROTECT, verbose_name='Производитель')
    country = models.ForeignKey(Country,on_delete=models.PROTECT, verbose_name='Страна')
    material = models.ForeignKey(Material, on_delete=models.SET_NULL, null=True, verbose_name='Материал',blank=True)
    in_stock = models.PositiveSmallIntegerField(default=0,verbose_name='Количество товара в наличии')
   #views = models.ForeignKey(Views,on_delete=models.SET_NULL, null=True)
    views = models.PositiveBigIntegerField(default=0, verbose_name='Количество просмотров')
    # favorites = models.ForeignKey(Favorites,on_delete=models.SET_NULL, null=True )
    # rating =
    url = models.SlugField(max_length=150, unique=True)
    # promotions = models.CharField(max_length=20, verbose_name='Акции') добавить позже

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('ShoesDetailview', kwargs={"pk": self.pk})

    class Meta:
        verbose_name = 'Обувь'
        verbose_name_plural = 'Обувь'
        ordering = ['-created']






class Users(models.Model):
    login = models.CharField(max_length=50, verbose_name='Логин')
    first_name = models.CharField(max_length=50, verbose_name='Имя', blank=True)
    second_name = models.CharField(max_length=50, verbose_name='Фамилия',  blank=True)
    password = models.CharField(max_length=50, verbose_name='Пароль')
    email = models.EmailField(verbose_name='Е-мейл',  blank=True)
    telephone = models.CharField(max_length=50, verbose_name='Номер телефона')
    address = models.CharField(max_length=50, verbose_name='Адресс',  blank=True)
    ip = models.CharField(max_length=50, verbose_name='IP пользователя')
    url = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return self.login

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Commentary(models.Model):
    shoes = models.ForeignKey(Shoes, on_delete=models.CASCADE, verbose_name='ID товара')
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name='ID пользователя')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name='ID комментария родителя', blank=True)
    title = models.CharField(max_length=150, verbose_name='Название комментария')
    text = models.TextField(max_length=1000, verbose_name='Комментарий')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

class Rating(models.Model):
    shoes = models.ForeignKey(Shoes,on_delete=models.CASCADE, verbose_name='ID товара')
    user_id = models.ForeignKey(Users,on_delete=models.CASCADE, verbose_name='ID пользователя')
    value = models.PositiveSmallIntegerField(default=0,verbose_name='Оценка')

    def __str__(self):
        return self.shoes

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'


class Favorites(models.Model):
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name='ID пользователя')
    shoes = models.ForeignKey(Shoes, on_delete=models.CASCADE, verbose_name='ID товара')

    def __str__(self):
        return f'{self.user_id} - {self.shoes}'

    class Meta:
        verbose_name = 'Избранный товар'
        verbose_name_plural = 'Избранные товары'


class Cart(models.Model):
    shoes = models.ForeignKey(Shoes, on_delete=models.CASCADE, verbose_name='ID товара')
    number =models.PositiveSmallIntegerField(default=1,verbose_name='Количество')
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name='ID пользователя')

    def __str__(self):
        return f'{self.user_id} - {self.shoes}'

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'

class Order(models.Model):
    cart = models.ManyToManyField(Cart, verbose_name='Товары с корзины')
    price = models.PositiveIntegerField(default=0, verbose_name='Стоимость заказа')
    payment = models.BooleanField(default=0, help_text='0 - онлайн перевод, 1 - наложенный платеж' )
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name='ID пользователя')
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

    # def get_absolute_url(self):
    #     return reverse('news_num', kwargs={"pk": self.pk})


# Create your models here.

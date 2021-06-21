from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User



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


class Shoes(models.Model):
    title = models.CharField(max_length=150, verbose_name='Наименование')
    price = models.PositiveSmallIntegerField(default=0,verbose_name='Цена')
    created = models.DateTimeField(auto_now_add=True,verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True,verbose_name='Дата обновления')
    content = models.TextField(max_length=1000, blank=True, verbose_name='Описание')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Категория')
    size = models.ManyToManyField(Size, verbose_name='Размеры')
    season = models.ForeignKey(Season,on_delete=models.PROTECT,verbose_name='Сезон')
    sex = models.BooleanField(default=False, help_text='1 - мальчик, 0 - девочка', verbose_name='Пол')
    brand = models.ForeignKey(Brand,on_delete=models.PROTECT, verbose_name='Производитель')
    country = models.ForeignKey(Country,on_delete=models.PROTECT, verbose_name='Страна')
   # material = models.ForeignKey(Material, on_delete=models.SET_NULL, null=True, verbose_name='Материал',blank=True)
   # in_stock = models.PositiveSmallIntegerField(default=0,verbose_name='Количество товара в наличии')          будем считать отдельно
   #views = models.ForeignKey(Views,on_delete=models.SET_NULL, null=True)
    views = models.PositiveBigIntegerField(default=0, verbose_name='Количество просмотров')
    # favorites = models.ForeignKey(Favorites,on_delete=models.SET_NULL, null=True )
    # rating =
    slug = models.SlugField(max_length=150, unique=True)
    # promotions = models.CharField(max_length=20, verbose_name='Акции') добавить позже

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('ShoesDetailview', kwargs={"slug": self.slug})

    class Meta:
        verbose_name = 'Обувь'
        verbose_name_plural = 'Обувь'
        ordering = ['-created']


class Material(models.Model):
    shoes = models.ForeignKey(Shoes, on_delete=models.CASCADE, verbose_name='ID товара')
    top = models.CharField(max_length=50, verbose_name='Верх', blank=True)
    sole = models.CharField(max_length=50, verbose_name='Подошва', blank=True)
    strap = models.CharField(max_length=50, verbose_name='Ремешок', blank=True)
    lining = models.CharField(max_length=50, verbose_name='Подкладка', blank=True)

    class Meta:
        verbose_name = 'Материал'
        verbose_name_plural = 'Материалы'

    def __str__(self):
        return str(self.shoes)


class Shoes_Images(models.Model):
    shoes = models.ForeignKey(Shoes, on_delete=models.CASCADE, verbose_name='ID товара')
    image = models.ImageField(upload_to='photos/%Y/%M/%D', verbose_name='Фото',help_text='размер фото 1024X768')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def __str__(self):
        return str(self.shoes)

    class Meta:
        verbose_name = 'фотография'
        verbose_name_plural = 'Фотографии'

class Commentary(models.Model):
    shoes = models.ForeignKey(Shoes, on_delete=models.CASCADE, verbose_name='ID товара')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='ID пользователя')
   # parent = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name='ID родителя отзыва', default='None', blank=True, null=True)
    text = models.TextField(max_length=1000, verbose_name='Комментарий', blank=True)
    value = models.PositiveSmallIntegerField(default=0,verbose_name='Оценка', blank=True)
    date =  models.DateTimeField(auto_now=True, verbose_name='Дата создания или обновления')
    def __str__(self):
        return 'пользователь: ' + str(self.user_id)#+ ', отзыв: ' + self.text[20] + ', оценка: ' + str(self.value)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='ID пользователя')
    commentary = models.ForeignKey(Commentary, on_delete=models.CASCADE, verbose_name='ID родителя отзыва')
    text = models.TextField(max_length=1000, verbose_name='Комментарий', blank=True)
    date =  models.DateTimeField(auto_now=True, verbose_name='Дата создания или обновления')
    def __str__(self):
        return 'пользователь: ' + str(self.user_id)+ ', отзыв: ' + self.text[10]

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'











# Create your models here.

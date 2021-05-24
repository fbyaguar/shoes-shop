from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=150, verbose_name='Наименование')
    url = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Size(models.Model):
    twenty = models.BooleanField(default=False, verbose_name='20')
    twenty_one = models.BooleanField(default=False, verbose_name='21')
    twenty_two = models.BooleanField(default=False, verbose_name='22')
    twenty_three = models.BooleanField(default=False, verbose_name='23')
    twenty_four = models.BooleanField(default=False, verbose_name='24')
    twenty_five= models.BooleanField(default=False, verbose_name='25')
    url = models.SlugField(max_length=150, unique=True)

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
    top = models.CharField(max_length=50, verbose_name='Верх')
    sole = models.CharField(max_length=50, verbose_name='Подошва')
    strap = models.CharField(max_length=50, verbose_name='Ремешок')
    lining = models.CharField(max_length=50, verbose_name='Подкладка')

    class Meta:
        verbose_name = 'Материал'
        verbose_name_plural = 'Материалы'




class Shoes(models.Model):
    title = models.CharField(max_length=150, verbose_name='Наименование')
    price = models.PositiveSmallIntegerField(default=0,verbose_name='Цена')
    created = models.DateTimeField(auto_now_add=True,verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True,verbose_name='Дата обновления')
    photo = models.ImageField(upload_to='photos/%Y/%M/%D', blank=True, verbose_name='Фото')
    content = models.TextField(max_length=1000, blank=True, verbose_name='Описание')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Категория')
    size = models.ForeignKey(Size,on_delete=models.PROTECT, verbose_name='Размеры')
    season = models.ForeignKey(Season,on_delete=models.PROTECT,verbose_name='Сезон')
    sex = models.BooleanField(default=False, help_text='1 - мальчик, 0 - девочка', verbose_name='Пол')
    brand = models.ForeignKey(Brand,on_delete=models.PROTECT, verbose_name='Производитель')
    country = models.ForeignKey(Country,on_delete=models.PROTECT, verbose_name='Страна')
    material = models.ForeignKey(Material, on_delete=models.SET_NULL, null=True, verbose_name='Материал')
    in_stock = models.PositiveSmallIntegerField(default=0,verbose_name='Количество товара в наличии')
   #views = models.ForeignKey(Views,on_delete=models.SET_NULL, null=True)
    views = models.PositiveBigIntegerField(default=0, verbose_name='Количество просмотров')
    # favorites = models.ForeignKey(Favorites,on_delete=models.SET_NULL, null=True )
    # rating =
    url = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return self.title


    class Meta:
        verbose_name = 'Обувь'
        verbose_name_plural = 'Обувь'
        ordering = ['-created']










    # def get_absolute_url(self):
    #     return reverse('news_num', kwargs={"pk": self.pk})

# Create your models here.

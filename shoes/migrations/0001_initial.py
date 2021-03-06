# Generated by Django 3.2.3 on 2021-06-07 18:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Наименование')),
                ('url', models.SlugField(max_length=150, unique=True)),
                ('logo', models.ImageField(blank=True, upload_to='logo/%Y/%M/%D', verbose_name='Логотип')),
                ('content', models.TextField(blank=True, max_length=1000, verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Производитель',
                'verbose_name_plural': 'Производители',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Наименование')),
                ('url', models.SlugField(max_length=150, unique=True)),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Наименование')),
                ('url', models.SlugField(max_length=150, unique=True)),
                ('flag', models.ImageField(blank=True, upload_to='flag/%Y/%M/%D', verbose_name='Флаг')),
            ],
            options={
                'verbose_name': 'Страна',
                'verbose_name_plural': 'Страны',
            },
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Наименование')),
                ('url', models.SlugField(max_length=150, unique=True)),
            ],
            options={
                'verbose_name': 'Сезон',
                'verbose_name_plural': 'Сезоны',
            },
        ),
        migrations.CreateModel(
            name='Shoes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Наименование')),
                ('price', models.PositiveSmallIntegerField(default=0, verbose_name='Цена')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('content', models.TextField(blank=True, max_length=1000, verbose_name='Описание')),
                ('sex', models.BooleanField(default=False, help_text='1 - мальчик, 0 - девочка', verbose_name='Пол')),
                ('views', models.PositiveBigIntegerField(default=0, verbose_name='Количество просмотров')),
                ('url', models.SlugField(max_length=150, unique=True)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shoes.brand', verbose_name='Производитель')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shoes.category', verbose_name='Категория')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shoes.country', verbose_name='Страна')),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shoes.season', verbose_name='Сезон')),
            ],
            options={
                'verbose_name': 'Обувь',
                'verbose_name_plural': 'Обувь',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveSmallIntegerField(default=0, verbose_name='Размер ноги')),
                ('url', models.SlugField(max_length=150, unique=True)),
            ],
            options={
                'verbose_name': 'Размер',
                'verbose_name_plural': 'Размеры',
            },
        ),
        migrations.CreateModel(
            name='Shoes_Images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(help_text='размер фото 1024X768', upload_to='photos/%Y/%M/%D', verbose_name='Фото')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('shoes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shoes.shoes', verbose_name='ID товара')),
            ],
            options={
                'verbose_name': 'фотография',
                'verbose_name_plural': 'Фотографии',
            },
        ),
        migrations.AddField(
            model_name='shoes',
            name='size',
            field=models.ManyToManyField(to='shoes.Size', verbose_name='Размеры'),
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.PositiveSmallIntegerField(default=0, verbose_name='Оценка')),
                ('shoes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shoes.shoes', verbose_name='ID товара')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='ID пользователя')),
            ],
            options={
                'verbose_name': 'Рейтинг',
                'verbose_name_plural': 'Рейтинги',
            },
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('top', models.CharField(blank=True, max_length=50, verbose_name='Верх')),
                ('sole', models.CharField(blank=True, max_length=50, verbose_name='Подошва')),
                ('strap', models.CharField(blank=True, max_length=50, verbose_name='Ремешок')),
                ('lining', models.CharField(blank=True, max_length=50, verbose_name='Подкладка')),
                ('shoes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shoes.shoes', verbose_name='ID товара')),
            ],
            options={
                'verbose_name': 'Материал',
                'verbose_name_plural': 'Материалы',
            },
        ),
        migrations.CreateModel(
            name='Commentary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Название комментария')),
                ('text', models.TextField(max_length=1000, verbose_name='Комментарий')),
                ('parent', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='shoes.commentary', verbose_name='ID комментария родителя')),
                ('shoes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shoes.shoes', verbose_name='ID товара')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='ID пользователя')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
            },
        ),
    ]

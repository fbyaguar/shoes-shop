# Generated by Django 3.2.3 on 2021-08-31 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shoes', '0011_shoes_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shoes',
            name='sex',
            field=models.CharField(choices=[('1', 'мальчик'), ('2', 'девочка')], max_length=100, verbose_name='Пол'),
        ),
    ]

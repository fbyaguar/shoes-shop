# Generated by Django 3.2.3 on 2021-09-21 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_rename_favorites_wishlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='wishlist',
            name='size',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Размер'),
        ),
    ]
# Generated by Django 3.2.3 on 2021-06-19 09:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shoes', '0003_alter_commentary_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentary',
            name='parent',
            field=models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.CASCADE, to='shoes.commentary', verbose_name='ID родителя отзыва'),
        ),
    ]

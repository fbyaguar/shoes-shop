# Generated by Django 3.2.3 on 2021-08-07 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shoes', '0010_alter_answer_commentary'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoes',
            name='rating',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Рейтинг'),
        ),
    ]

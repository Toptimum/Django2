# Generated by Django 2.2.4 on 2019-08-11 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0010_auto_20190811_1546'),
    ]

    operations = [
        migrations.AddField(
            model_name='infopages',
            name='order_in_menu',
            field=models.PositiveIntegerField(default=0, verbose_name='Номер в меню'),
        ),
    ]
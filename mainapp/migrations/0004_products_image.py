# Generated by Django 2.2.3 on 2019-07-30 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_auto_20190730_1248'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='image',
            field=models.ImageField(blank=True, upload_to='products_images'),
        ),
    ]
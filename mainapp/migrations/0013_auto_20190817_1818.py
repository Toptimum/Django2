# Generated by Django 2.2.4 on 2019-08-17 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0012_auto_20190815_1013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='image_product',
            field=models.ImageField(blank=True, default='images_products/no_image.jpg', upload_to='images_products'),
        ),
    ]
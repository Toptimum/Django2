# Generated by Django 2.2.3 on 2019-07-31 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0007_categories_header_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='categories',
            name='link_category',
            field=models.CharField(blank=True, max_length=128, verbose_name='Ссылка категории'),
        ),
    ]

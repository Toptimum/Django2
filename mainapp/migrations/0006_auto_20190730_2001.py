# Generated by Django 2.2.3 on 2019-07-30 17:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0005_auto_20190730_1307'),
    ]

    operations = [
        migrations.RenameField(
            model_name='products',
            old_name='id_category',
            new_name='category',
        ),
    ]

# Generated by Django 2.2.3 on 2019-07-30 09:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='categories',
            old_name='decription_category',
            new_name='description_category',
        ),
    ]
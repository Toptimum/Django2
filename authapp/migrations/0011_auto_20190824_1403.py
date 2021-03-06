# Generated by Django 2.2.4 on 2019-08-24 11:03

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0010_auto_20190824_1335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuser',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 26, 11, 3, 19, 582167, tzinfo=utc)),
        ),
        migrations.CreateModel(
            name='ShopUserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tagline', models.CharField(blank=True, max_length=128, verbose_name='Теги')),
                ('aboutMe', models.TextField(blank=True, max_length=512, verbose_name='О себе')),
                ('gender', models.CharField(blank=True, choices=[('M', 'М'), ('W', 'Ж')], max_length=1, verbose_name='Пол')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

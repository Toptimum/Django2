# Generated by Django 2.2.4 on 2019-08-24 09:46

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0004_auto_20190824_1239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuser',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 26, 9, 46, 54, 325561, tzinfo=utc)),
        ),
    ]

# Generated by Django 3.2.5 on 2021-07-10 17:55

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0013_auto_20210710_2021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 12, 17, 55, 15, 603999, tzinfo=utc)),
        ),
    ]

# Generated by Django 3.2.6 on 2021-09-18 09:01

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_activation_key_expires'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 20, 9, 1, 35, 285800, tzinfo=utc)),
        ),
    ]

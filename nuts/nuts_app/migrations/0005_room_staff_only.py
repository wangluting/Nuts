# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-29 20:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nuts_app', '0004_remove_room_staff_only'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='staff_only',
            field=models.BooleanField(default=False),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-30 00:44
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nuts_app', '0005_room_staff_only'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='staff_only',
        ),
    ]

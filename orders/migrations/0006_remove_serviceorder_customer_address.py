# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-10-21 16:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_auto_20171021_1853'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='serviceorder',
            name='customer_address',
        ),
    ]

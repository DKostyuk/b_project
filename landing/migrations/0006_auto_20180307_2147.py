# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-03-07 20:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0005_auto_20180307_2138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriber',
            name='city',
            field=models.CharField(default=None, max_length=56, null=True),
        ),
    ]

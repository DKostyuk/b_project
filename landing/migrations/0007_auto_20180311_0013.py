# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-03-10 23:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0006_auto_20180307_2147'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriber',
            name='tel_number',
            field=models.IntegerField(blank=True, default=None, max_length=9, null=True),
        ),
        migrations.AlterField(
            model_name='subscriber',
            name='index',
            field=models.IntegerField(blank=True, default=None, max_length=5, null=True),
        ),
    ]

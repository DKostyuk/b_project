# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-04-19 05:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0015_auto_20180419_0705'),
    ]

    operations = [
        migrations.AddField(
            model_name='training',
            name='image',
            field=models.ImageField(default='../img/bg_image.png', upload_to='training/'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-04-20 19:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0016_training_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='training',
            name='image',
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-04-25 17:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('another', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='anothertrick',
            name='url',
        ),
        migrations.AddField(
            model_name='anothertrick',
            name='slug',
            field=models.SlugField(default=1, max_length=64, unique=True),
            preserve_default=False,
        ),
    ]

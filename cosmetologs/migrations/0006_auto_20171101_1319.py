# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-11-01 11:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cosmetologs', '0005_subcategoryforcosmetolog'),
    ]

    operations = [
        migrations.AddField(
            model_name='subcategoryforcosmetolog',
            name='subcategory_category',
            field=models.CharField(blank=True, default=None, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='subcategoryforcosmetolog',
            name='url',
            field=models.CharField(blank=True, default=None, max_length=64, null=True),
        ),
    ]

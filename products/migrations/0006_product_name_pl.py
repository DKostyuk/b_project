# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-03-12 17:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_productcategory_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='name_pl',
            field=models.CharField(blank=True, default=None, max_length=64, null=True),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-03-12 16:59
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20180226_1852'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcategory',
            name='description',
            field=ckeditor.fields.RichTextField(blank=True, default=None, null=True),
        ),
    ]

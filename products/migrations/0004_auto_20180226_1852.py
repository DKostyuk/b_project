# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-02-26 17:52
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20180206_1831'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description_1',
            field=ckeditor.fields.RichTextField(default=1),
            preserve_default=False,
        ),
    ]

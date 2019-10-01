# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-10-08 10:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0003_auto_20171008_1303'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='parent_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='addresses.Address'),
        ),
    ]

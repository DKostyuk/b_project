# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-11-01 11:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_auto_20171021_2004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serviceorder',
            name='service_id',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='cosmetologs.ServiceProduct'),
        ),
    ]

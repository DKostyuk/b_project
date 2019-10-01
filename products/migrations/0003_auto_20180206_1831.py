# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-02-06 17:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20171101_1303'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='description_1',
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='description_2',
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='description_3',
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='description_4',
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='description_5',
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='name_description',
            field=models.CharField(blank=True, default=None, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='name_description_1',
            field=models.CharField(blank=True, default=None, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='name_description_2',
            field=models.CharField(blank=True, default=None, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='name_description_3',
            field=models.CharField(blank=True, default=None, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='name_description_4',
            field=models.CharField(blank=True, default=None, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='name_description_5',
            field=models.CharField(blank=True, default=None, max_length=64, null=True),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-10-08 09:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AddressType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default=None, max_length=32, null=True)),
                ('slug', models.SlugField(max_length=32, unique=True)),
                ('variants', models.CharField(blank=True, default=None, max_length=128, null=True)),
                ('level', models.IntegerField(blank=True, default=None, max_length=2, null=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'AddressType',
                'verbose_name_plural': 'AddressTypes',
            },
        ),
    ]

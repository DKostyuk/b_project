# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-10-09 08:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0008_auto_20171009_1155'),
        ('cosmetologs', '0002_serviceproduct_is_visible'),
    ]

    operations = [
        migrations.CreateModel(
            name='CosmetologAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cosmetolog_id', models.IntegerField(blank=True, default=None, null=True)),
                ('address_id', models.IntegerField(blank=True, default=None, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_main', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('address_name', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='addresses.Address')),
                ('cosmetolog_name', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='cosmetologs.Cosmetolog')),
            ],
            options={
                'verbose_name': 'CosmetologAddress',
                'verbose_name_plural': 'CosmetologAddresses',
            },
        ),
    ]

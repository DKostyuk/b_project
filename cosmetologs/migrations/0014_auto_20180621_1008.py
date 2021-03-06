# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-06-21 08:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cosmetologs', '0013_auto_20180531_1756'),
    ]

    operations = [
        migrations.CreateModel(
            name='CosmetologEmail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(blank=True, default=None, max_length=254, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_main', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'CosmetologEmail',
                'verbose_name_plural': 'CosmetologEmails',
            },
        ),
        migrations.CreateModel(
            name='CosmetologPhone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(blank=True, default=None, max_length=10, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_main', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'CosmetologPhone',
                'verbose_name_plural': 'CosmetologPhones',
            },
        ),
        migrations.AlterField(
            model_name='cosmetolog',
            name='order_email',
            field=models.EmailField(blank=True, default=None, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='cosmetologphone',
            name='cosmetolog',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='cosmetologs.Cosmetolog'),
        ),
        migrations.AddField(
            model_name='cosmetologemail',
            name='cosmetolog',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='cosmetologs.Cosmetolog'),
        ),
    ]

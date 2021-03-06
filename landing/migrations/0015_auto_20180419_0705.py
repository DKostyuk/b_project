# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-04-19 05:05
from __future__ import unicode_literals

import ckeditor.fields
import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0014_page'),
    ]

    operations = [
        migrations.CreateModel(
            name='Training',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('slug', models.SlugField(max_length=64, unique=True)),
                ('type', models.CharField(max_length=16)),
                ('description', ckeditor_uploader.fields.RichTextUploadingField(blank=True, default=None, null=True)),
                ('start_date', models.DateTimeField(default=None)),
                ('duration', models.CharField(max_length=8)),
                ('location', models.CharField(max_length=64)),
                ('audience', models.CharField(max_length=32)),
                ('goal', models.CharField(max_length=128)),
                ('agenda', ckeditor.fields.RichTextField(blank=True, default=None, null=True)),
                ('trainer', models.CharField(max_length=32)),
                ('total_place', models.IntegerField(blank=True, default=None, null=True)),
                ('registered_place', models.IntegerField(blank=True, default=None, null=True)),
                ('left_place', models.IntegerField(blank=True, default=None, null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Training',
                'verbose_name_plural': 'Trainings',
            },
        ),
        migrations.AlterModelOptions(
            name='page',
            options={'verbose_name': 'Page', 'verbose_name_plural': 'Pages'},
        ),
        migrations.AlterField(
            model_name='page',
            name='page_text',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, default=None, null=True),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-04-21 07:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0018_training_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrainingUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trainee_name', models.CharField(max_length=64)),
                ('trainee_email', models.EmailField(max_length=254)),
                ('email_confirm', models.BooleanField(default=False)),
                ('trainee_tel_number', models.CharField(blank=True, default=None, max_length=11, null=True)),
                ('tel_number_confirm', models.BooleanField(default=False)),
                ('registration_confirmed', models.BooleanField(default=False)),
                ('comments', models.TextField(blank=True, default=None, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('user_name', models.CharField(max_length=32)),
                ('user_email', models.EmailField(max_length=254)),
                ('training', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='landing.Training')),
            ],
            options={
                'verbose_name': 'TrainingUser',
                'verbose_name_plural': 'TrainingUsers',
            },
        ),
    ]

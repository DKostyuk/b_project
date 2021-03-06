# Generated by Django 2.1.4 on 2018-12-15 18:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cosmetologs', '0018_auto_20181214_1425'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceAddFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comments', models.CharField(blank=True, default=None, max_length=124, null=True)),
                ('product_file', models.FileField(upload_to='product_file_add/')),
                ('is_active', models.BooleanField(default=False)),
                ('start_import', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('modified_by', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'ServiceAddFile',
                'verbose_name_plural': 'ServiceAddFiles',
            },
        ),
        migrations.AddField(
            model_name='cosmetolog',
            name='description_product',
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='cosmetolog',
            name='description_service',
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
    ]

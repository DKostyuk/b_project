# Generated by Django 2.1.4 on 2019-03-04 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cosmetologs', '0028_auto_20190304_1253'),
    ]

    operations = [
        migrations.AddField(
            model_name='cosmetologaddress',
            name='address_type_id',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]

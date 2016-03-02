# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_product_thumbnail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='is_bestseller',
        ),
        migrations.RemoveField(
            model_name='product',
            name='is_featured',
        ),
        migrations.AddField(
            model_name='product',
            name='gender',
            field=models.CharField(max_length=20, default='unisex'),
        ),
    ]

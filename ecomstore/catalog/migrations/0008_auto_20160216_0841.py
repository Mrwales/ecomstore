# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_auto_20160215_2129'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='b_slug',
            field=models.SlugField(null=True, max_length=255),
        ),
        migrations.RemoveField(
            model_name='product',
            name='brand',
        ),
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.CharField(null=True, max_length=255),
        ),
        migrations.DeleteModel(
            name='Brand',
        ),
    ]

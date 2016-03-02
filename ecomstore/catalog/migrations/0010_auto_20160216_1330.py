# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import catalog.myThumbs


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0009_auto_20160216_1242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='thumbnail1',
            field=catalog.myThumbs.ThumbnailImageField(null=True, upload_to='images/products/thumbnails'),
        ),
        migrations.AlterField(
            model_name='product',
            name='thumbnail2',
            field=catalog.myThumbs.ThumbnailImageField(null=True, upload_to='images/products/thumbnails'),
        ),
    ]

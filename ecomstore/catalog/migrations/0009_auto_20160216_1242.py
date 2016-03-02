# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import catalog.myThumbs


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0008_auto_20160216_0841'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='thumbnail1',
            field=catalog.myThumbs.ThumbnailImageField(default='', upload_to='images/products/thumbnails'),
        ),
        migrations.AddField(
            model_name='product',
            name='thumbnail2',
            field=catalog.myThumbs.ThumbnailImageField(default='', upload_to='images/products/thumbnails'),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
#import catalog.myThumbs


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
#         migrations.AddField(
#             model_name='product',
#             name='thumbnail',
#             field=catalog.myThumbs.ThumbnailImageField(default='', upload_to='images/products/thumbnails'),
#         ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(upload_to='images/products/main'),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapplication', '0011_auto_20160405_1538'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='containsencrypted',
            field=models.CharField(default='no', max_length=3, choices=[('yes', 'yes'), ('no', 'no')]),
        ),
    ]

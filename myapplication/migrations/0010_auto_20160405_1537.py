# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapplication', '0009_auto_20160405_1534'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='containsencrypted',
            field=models.BooleanField(default=False),
        ),
    ]

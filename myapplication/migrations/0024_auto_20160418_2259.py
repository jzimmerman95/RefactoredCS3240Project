# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapplication', '0023_auto_20160413_0100'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='containsencrypted',
        ),
        migrations.AddField(
            model_name='reportfiles',
            name='isencrypted',
            field=models.BooleanField(default=False),
        ),
    ]

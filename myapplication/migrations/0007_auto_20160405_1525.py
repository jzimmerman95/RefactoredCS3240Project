# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapplication', '0006_report_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='containsencrypted',
            field=models.BooleanField(default=False),
        ),
    ]

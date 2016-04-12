# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapplication', '0004_report_numfiles'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='numfiles',
        ),
    ]

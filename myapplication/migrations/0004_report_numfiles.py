# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapplication', '0003_report_reportfiles'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='numfiles',
            field=models.CharField(default='none', max_length=200),
        ),
    ]

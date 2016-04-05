# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapplication', '0012_auto_20160405_1547'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='isprivate',
            field=models.CharField(max_length=7, default='public', choices=[('public', 'public'), ('private', 'private')]),
        ),
        migrations.AddField(
            model_name='report',
            name='owner',
            field=models.CharField(max_length=100, default='none'),
        ),
    ]

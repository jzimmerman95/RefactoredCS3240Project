# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapplication', '0019_folders'),
    ]

    operations = [
        migrations.AddField(
            model_name='folders',
            name='owner',
            field=models.CharField(max_length=200, default='none'),
        ),
    ]

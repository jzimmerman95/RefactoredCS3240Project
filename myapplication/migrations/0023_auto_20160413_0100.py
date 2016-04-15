# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapplication', '0022_auto_20160413_0054'),
    ]

    operations = [
        migrations.RenameField(
            model_name='folders',
            old_name='reportname',
            new_name='reports',
        ),
    ]

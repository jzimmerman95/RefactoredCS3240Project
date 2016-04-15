# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapplication', '0020_folders_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinformation',
            name='password',
        ),
    ]

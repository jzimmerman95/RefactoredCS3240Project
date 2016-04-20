# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapplication', '0027_auto_20160419_0000'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinformation',
            name='role',
            field=models.CharField(default='user', max_length=50),
        ),
    ]

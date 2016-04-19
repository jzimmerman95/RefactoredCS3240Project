# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapplication', '0026_auto_20160418_2358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reportfiles',
            name='isencrypted',
            field=models.BooleanField(default=False, choices=[('yes', 'yes'), ('no', 'no')]),
        ),
    ]

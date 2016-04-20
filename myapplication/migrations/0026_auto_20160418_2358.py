# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapplication', '0025_auto_20160418_2330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reportfiles',
            name='isencrypted',
            field=models.CharField(choices=[('yes', 'yes'), ('no', 'no')], max_length=3),
        ),
    ]

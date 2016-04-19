# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapplication', '0024_auto_20160418_2259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reportfiles',
            name='isencrypted',
            field=models.CharField(default='no', max_length=3),
        ),
    ]

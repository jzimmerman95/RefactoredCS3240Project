# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapplication', '0010_auto_20160405_1537'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='containsencrypted',
            field=models.NullBooleanField(),
        ),
    ]

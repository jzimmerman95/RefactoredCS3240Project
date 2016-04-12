# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapplication', '0015_auto_20160405_1832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reportfiles',
            name='uploadfile',
            field=models.FileField(upload_to='.'),
        ),
    ]

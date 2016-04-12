# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapplication', '0014_reportgroups'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reportfiles',
            name='uploadfile',
            field=models.ImageField(upload_to='.'),
        ),
    ]

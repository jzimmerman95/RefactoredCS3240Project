# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapplication', '0031_messages'),
    ]

    operations = [
        migrations.AddField(
            model_name='messages',
            name='encrypted',
            field=models.BooleanField(choices=[('yes', 'yes'), ('no', 'no')], default=False),
        ),
    ]

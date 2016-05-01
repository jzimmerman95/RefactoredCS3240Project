# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('myapplication', '0032_messages_encrypted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messages',
            name='created',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='messages',
            name='encrypted',
            field=models.BooleanField(default=False),
        ),
    ]

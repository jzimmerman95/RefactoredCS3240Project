# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import myapplication.models


class Migration(migrations.Migration):

    dependencies = [
        ('myapplication', '0016_auto_20160405_1842'),
    ]

    operations = [
        migrations.CreateModel(
            name='Folders',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('foldername', models.CharField(max_length=100)),
                # ('reports', myapplication.models.ListField()),
            ],
        ),
    ]

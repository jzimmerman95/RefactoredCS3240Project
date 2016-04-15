# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapplication', '0018_delete_folders'),
    ]

    operations = [
        migrations.CreateModel(
            name='Folders',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('foldername', models.CharField(max_length=100)),
                ('reports', models.CharField(max_length=255)),
            ],
        ),
    ]

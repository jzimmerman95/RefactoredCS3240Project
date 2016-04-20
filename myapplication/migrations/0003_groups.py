# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapplication', '0002_auto_20160329_1714'),
    ]

    operations = [
        migrations.CreateModel(
            name='Groups',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('groupname', models.CharField(max_length=200, default='none')),
                ('owner', models.CharField(max_length=200, default='none')),
                ('username', models.CharField(max_length=200, default='none')),
            ],
        ),
    ]

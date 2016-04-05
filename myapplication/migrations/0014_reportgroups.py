# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapplication', '0013_auto_20160405_1602'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReportGroups',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('reportname', models.CharField(max_length=100)),
                ('groupname', models.CharField(max_length=200)),
            ],
        ),
    ]

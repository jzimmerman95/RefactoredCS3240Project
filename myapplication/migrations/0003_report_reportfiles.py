# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapplication', '0002_auto_20160329_1714'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('reportname', models.CharField(max_length=100)),
                ('summary', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('containsencrypted', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='ReportFiles',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('reportname', models.CharField(max_length=100)),
                ('uploadfile', models.FileField(upload_to='')),
            ],
        ),
    ]

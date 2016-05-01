# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapplication', '0030_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('sender', models.CharField(max_length=100)),
                ('recipient_username', models.CharField(max_length=100)),
                ('subject', models.CharField(default=None, max_length=100)),
                ('body', models.TextField(max_length=1000)),
                ('created', models.DateTimeField(default=None)),
            ],
        ),
    ]

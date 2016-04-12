# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserInformation',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('username', models.CharField(max_length=200)),
                ('password', models.CharField(default='none', max_length=200)),
                ('email', models.CharField(default='none', max_length=200)),
                ('firstname', models.CharField(default='none', max_length=200)),
                ('lastname', models.CharField(default='none', max_length=200)),
            ],
        ),
    ]

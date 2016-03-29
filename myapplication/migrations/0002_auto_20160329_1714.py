# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapplication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinformation',
            name='publickey',
            field=models.CharField(max_length=200, default='none'),
        ),
        migrations.AlterField(
            model_name='userinformation',
            name='email',
            field=models.EmailField(max_length=200, default='none'),
        ),
        migrations.AlterField(
            model_name='userinformation',
            name='username',
            field=models.CharField(max_length=200, default='none'),
        ),
    ]

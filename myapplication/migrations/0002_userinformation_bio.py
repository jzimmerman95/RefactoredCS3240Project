# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapplication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinformation',
            name='bio',
            field=models.CharField(max_length=1000, default='none'),
        ),
    ]

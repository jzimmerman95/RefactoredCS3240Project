# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapplication', '0028_userinformation_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinformation',
            name='numsitemanagersmade',
            field=models.IntegerField(default=0),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapplication', '0021_remove_userinformation_password'),
    ]

    operations = [
        migrations.RenameField(
            model_name='folders',
            old_name='reports',
            new_name='reportname',
        ),
    ]

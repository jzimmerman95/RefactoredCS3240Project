# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Folders',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('foldername', models.CharField(max_length=100)),
                ('owner', models.CharField(max_length=200, default='none')),
                ('reports', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Groups',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('groupname', models.CharField(max_length=200, default='none')),
                ('owner', models.CharField(max_length=200, default='none')),
                ('username', models.CharField(max_length=200, default='none')),
            ],
        ),
        migrations.CreateModel(
            name='GroupUsers',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('groupname', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('sender', models.CharField(max_length=100)),
                ('recipient_username', models.CharField(max_length=100)),
                ('subject', models.CharField(max_length=100, default=None)),
                ('body', models.TextField(max_length=1000)),
                ('created', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('encrypted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('reportname', models.CharField(max_length=100)),
                ('owner', models.CharField(max_length=100, default='none')),
                ('summary', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('isprivate', models.CharField(default='public', max_length=7, choices=[('public', 'public'), ('private', 'private')])),
                ('timestamp', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='ReportFiles',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('reportname', models.CharField(max_length=100)),
                ('isencrypted', models.BooleanField(default=False, choices=[('yes', 'yes'), ('no', 'no')])),
                ('uploadfile', models.FileField(upload_to='.')),
            ],
        ),
        migrations.CreateModel(
            name='ReportGroups',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('reportname', models.CharField(max_length=100)),
                ('groupname', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='UserInformation',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('username', models.CharField(max_length=200, default='none')),
                ('email', models.EmailField(max_length=200, default='none')),
                ('firstname', models.CharField(max_length=200, default='none')),
                ('lastname', models.CharField(max_length=200, default='none')),
                ('publickey', models.CharField(max_length=200, default='none')),
                ('role', models.CharField(max_length=50, default='user')),
                ('numsitemanagersmade', models.IntegerField(default=0)),
            ],
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-03 16:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodbot', '0002_remove_userinfo_counter_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinfo',
            name='location',
        ),
        migrations.AddField(
            model_name='userinfo',
            name='counter',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userinfo',
            name='lat',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userinfo',
            name='long',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userinfo',
            name='state',
            field=models.IntegerField(default=None),
            preserve_default=False,
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-03 17:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodbot', '0005_auto_20170603_1715'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='state',
            field=models.IntegerField(default=0, null=True),
        ),
    ]

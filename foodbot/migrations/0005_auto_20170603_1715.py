# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-03 17:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodbot', '0004_userinfo_served'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='counter',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='served',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='state',
            field=models.IntegerField(default=0),
        ),
    ]

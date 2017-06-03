# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class UserInfo(models.Model):
    name = models.CharField(max_length=100)
    lat = models.FloatField()
    long = models.FloatField()
    served = models.IntegerField(default=0)
    counter = models.IntegerField(default=0)
    state = models.IntegerField(default=0)
    # address = models.CharField(max_length=100, null=True, blank=True, default=' ')
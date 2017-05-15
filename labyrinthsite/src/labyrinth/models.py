# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User 

# Create your models here.

class MyUser(models.Model):
    CHOICES = (('male', 'Мужской'), ('female', 'Женский'))
    
    user = models.OneToOneField(User)
    phone = models.CharField(max_length=15)
    age = models.IntegerField(default=0)
    gender = models.CharField(max_length = 7)
    bomb = models.SmallIntegerField(default=0) 
    concrete = models.SmallIntegerField(default=0) 
    aid = models.SmallIntegerField(default=0) 
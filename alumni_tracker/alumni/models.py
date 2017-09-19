# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Alumnus(models.Model):
	name = models.CharField(max_length=100)
	roll_no = models.CharField(max_length=7)
	city = models.CharField(max_length=15)
	country = models.CharField(max_length=15)
	email_id = models.CharField(max_length=20)
	dept_code = models.CharField(max_length=7)
	grad_year = models.IntegerField(max_length=4)
	cgpa = models.IntegerField(max_length=4)

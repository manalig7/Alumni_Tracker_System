# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Alumnus(models.Model):
	name = models.CharField(max_length=100)
	roll_no = models.CharField(max_length=7,primary_key=True)
	city = models.CharField(max_length=15)
	country = models.CharField(max_length=15)
	email_id = models.CharField(max_length=20)
	dept_code = models.CharField(max_length=7)
	grad_year = models.IntegerField(max_length=4)
	cgpa = models.IntegerField(max_length=4)

class Studied(models.Model):
	roll_no = models.ForeignKey(Alumnus,on_delete=models.SET_NULL)
	school_name = models.ForeignKey(School,on_delete=models.SET_NULL)
	programme = models.CharField(max_length=50)
	grad_year = models.IntergerField(max_length=4)

	class Meta:
		unique_together = (('roll_no', 'school_name'),)

class Job(models.Model) :
	roll_no = models.ForeignKey(Alumnus,on_delete=models.SET_NULL)
	company_name = models.ForeignKey(Company,on_delete=models.SET_NULL)
	city = models.ForeignKey(Company,on_delete=models.SET_NULL)
	field = models.CharField(max_length=15)
	position = models.CharField(max_length=15)
	
	class Meta:
		unique_together = (('roll_no', 'company_name','city'),)

class School(models.Model):
	school_name = models.CharField(max_length=100,primary_key=True)
	city = models.CharField(max_length=15)
	country = models.CharField(max_length=15)

class Department(models.Model):
	dept_code = models.CharField(max_length=7,primary_key=True)
	dept_name = models.CharField(max_length=50)


class Company(models.Model):
	name=models.CharField(max_length=20)
	city=models.CharField(max_length=10)
	country = models.CharField(max_length=15)

	class Meta:
        unique_together = (('name', 'city'),)


class Alumnus_majors(models.Model):
	roll_no = models.ForeignKey(Alumnus,on_delete=models.SET_NULL)
	major = models.CharField(max_length=30)

	class Meta:
        unique_together = (('roll_no', 'major'),)

class Alumnus_links(models.Model):
	roll_no = models.ForeignKey(Alumnus,on_delete=models.SET_NULL)
	link = models.CharField(max_length=30)

	class Meta:
        unique_together = (('roll_no', 'link'),)


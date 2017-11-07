from django.db import models
from django.core.urlresolvers import reverse
# Create your models here.

class Location(models.Model):
	city = models.CharField(max_length=30,primary_key=True)
	country = models.CharField(max_length=30)

	def __str__(self):
		return self.city

class Department(models.Model):
	dept_code = models.CharField(max_length=7,primary_key=True)
	dept_name = models.CharField(max_length=50)

	def __str__(self):
		return self.dept_code

class Alumnus(models.Model):
	alumni_name = models.CharField(max_length=100)
	roll_no = models.CharField(max_length=7,primary_key=True)
	present_city = models.ForeignKey(Location,on_delete=models.SET_NULL,null=True)
	email_id = models.CharField(max_length=20,null=True)
	dept_code = models.ForeignKey(Department,on_delete=models.SET_NULL,null=True)
	grad_year = models.IntegerField()
	cgpa = models.IntegerField()
	github = models.CharField(max_length=30)
	linkedin = models.CharField(max_length=30)

	def get_absolute_url(self):
		return reverse('alumni_tracker:search',kwargs={'pk': self.pk})

	def __str__(self):
		return self.alumni_name + ' ' + self.roll_no

class School(models.Model):
	school_name = models.CharField(max_length=100,primary_key=True)
	city = models.ForeignKey(Location,on_delete=models.SET_NULL,null=True)

	def __str__(self):
		return self.school_name
	
class Company(models.Model):
	name = models.CharField(max_length=20)
	city = models.ForeignKey(Location,on_delete=models.SET_NULL,null=True)

	def __str__(self):
		return self.name

class Studied(models.Model):
	roll_no = models.ForeignKey(Alumnus,on_delete=models.CASCADE)
	school_name = models.ForeignKey(School,on_delete=models.CASCADE)
	programme = models.CharField(max_length=50)
	grad_year = models.IntegerField()
	
	class Meta:
		unique_together = ('roll_no', 'school_name',)

	def __str__(self):
		return self.programme+' '+str(self.grad_year)

class Job(models.Model) :
	roll_no = models.ForeignKey(Alumnus,on_delete=models.CASCADE)
	company_id = models.ForeignKey(Company,on_delete=models.CASCADE)
	field = models.CharField(max_length=15)
	position = models.CharField(max_length=15)
	
	class Meta:
		unique_together = ('roll_no', 'company_id',)

	def __str__(self):
		return self.field+' '+self.position

class Alumnus_majors(models.Model):
	roll_no = models.ForeignKey(Alumnus,on_delete=models.CASCADE)
	major = models.CharField(max_length=30)

	class Meta:
		unique_together = ('roll_no','major',)

	def __str__(self):
		return self.major

from django.contrib.auth.models import User
from .models import Alumnus
from django import forms

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)
	
	class Meta:
		model = User
		fields = ['username','email','password']

class UpdateProfileForm(forms.ModelForm):
	class Meta:
		model = Alumnus
		fields = ['alumni_name','roll_no','present_city','email_id','dept_code','grad_year','cgpa', "github", "linkedin"]

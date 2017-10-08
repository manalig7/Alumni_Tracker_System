

from django.http import HttpResponse
from django.shortcuts import render
from .models import Location, Alumnus, School, Department, Company, Studied, Job, Alumnus_majors, Alumnus_links
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView   #to create,edit a new object

class DetailView(generic.DetailView):
	model = Alumnus
	template_name = 'alumni_tracker/details.html'
	context_object_name = 'alumnus'

class IndexView(generic.ListView):
	template_name = 'alumni_tracker/display.html'
	context_object_name = 'alumni_list'
	
	def get_queryset(self):
		return Alumnus.objects.all()

class AlumnusCreate(CreateView):
	model = Alumnus
	fields = ['alumni_name','roll_no','present_city','email_id','dept_code','grad_year','cgpa']

def home(request):
	context = {}
	return render(request, 'alumni_tracker/home.html',context)

def registration(request):
    return HttpResponse("Hello, world. You're at the registration page")

def login(request):
    return HttpResponse("Hello, world. You can mnow login")

def search(request):
	all_alumni = Alumnus.objects.all()
	context = {}
	return render(request, 'alumni_tracker/search.html',context)


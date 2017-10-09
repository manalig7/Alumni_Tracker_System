

from django.http import HttpResponse
from django.shortcuts import render,redirect
from .models import Location, Alumnus, School, Department, Company, Studied, Job, Alumnus_majors, Alumnus_links
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView   #to create,edit a new object
from django.contrib.auth import authenticate, login    
from django.views.generic import View
from .forms import UserForm
from django.db.models import Q

class DetailView(generic.DetailView):
	model = Alumnus
	template_name = 'alumni_tracker/details.html'
	context_object_name = 'alumnus'

class IndexView(generic.ListView):
	template_name = 'alumni_tracker/display.html'
	context_object_name = 'alumni_list'
	
	def get_queryset(self):
		#alumni = Alumnus.objects.filter(user=self.user)
		alumni_results = Alumnus.objects.all()
		query = self.GET.get("name")
		if query:
			alumni = alumni.filter(
				Q(alumni_name__icontains=query)
			).distinct()
			alumni_results = alumni_results.filter(
				Q(alumni_name__icontains=query)
			).distinct()
			return render(self, 'alumni_tracker/display.html', {'alumni': alumni})
		else:
			return render(self, 'alumni_tracker/display.html', {'alumni_list': alumni})
		#return Alumnus.objects.all()

def display(request):
	alumni_results = Alumnus.objects.all()
	query = request.GET.get("name")
	if query:
		alumni_results = alumni_results.filter(
			Q(alumni_name__icontains=query)
		).distinct()
		return render(request, 'alumni_tracker/display.html', {'alumni_list': alumni_results})
	else:
		return render(request, 'alumni_tracker/display.html', {'alumni_list': alumni_results})
		#return Alumnus.objects.all()

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

class UserFormView(View):
	form_class = UserForm
	template_name = 'alumni_tracker/registration_form.html'

	#display blank form
	def get(self,request):
		form = self.form_class(None)
		return render(request, self.template_name, {'form':form})

	#process form data
	def post(self,request):
		form = self.form_class(request.POST)

		if form.is_valid():

			user = form.save(commit=False)

			#cleaned (normalized data)
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user.set_password(password)
			user.save()

			#returns user objects if credentials are correct
			user = authenticate(username=username, password=password)

			if user is not None:

				if user.is_active:
					login(request)
					return redirect('alumni_tracker:createalumnus')

		return render(request, self.template_name,{'form':form}) 
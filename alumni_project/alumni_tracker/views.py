

from django.http import HttpResponse
from django.shortcuts import render,redirect
from .models import Location, Alumnus, School, Department, Company, Studied, Job, Alumnus_majors
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView   #to create,edit a new object
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import authenticate, login    
from django.views.generic import View
from .forms import UserForm
from django.db.models import Q
from django.contrib.auth import views as auth_views
from django.core.exceptions import ObjectDoesNotExist

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
		query1=self.GET.get("present_city")
		if query:
			alumni = alumni.filter(
				Q(alumni_name__icontains=query)
			).distinct()
			alumni_results = alumni_results.filter(
				Q(alumni_name__icontains=query)
			).distinct()
		if query1:
				alumni_results = alumni_results.filter(
				Q(present_city__icontains=query1)
			).distinct()

		return render(self, 'alumni_tracker/display.html', {'alumni': alumni})
		#else:
		#return render(self, 'alumni_tracker/display.html', {'alumni_list': alumni})
		#return Alumnus.objects.all()

def display(request):
	alumni_results = Alumnus.objects.all()
	query = request.GET.get("name")
	query1= request.GET.get("grad_year")
	query2= request.GET.get("present_city")
	query3= request.GET.get("dept_code")
	flag=1
	if query:
		alumni_results = alumni_results.filter(
			Q(alumni_name__icontains=query) 
		).distinct()
	if query1:
		alumni_results = alumni_results.filter(
		Q(grad_year__exact=query1) 
	).distinct()
	if query2:
		alumni_results = alumni_results.filter(
		Q(present_city__city__icontains=query2) 
	).distinct()
	if query3:
		alumni_results = alumni_results.filter(
		Q(dept_code__dept_code__icontains=query3) 
	).distinct()
	#if query1:
	#	alumni_results = alumni_results.filter(
	#		Q(present_city__icontains=query1)
	#	).distinct()
	#	flag=1
	if flag==1:
		return render(request, 'alumni_tracker/display.html', {'alumni_list': alumni_results})
	else:
		return render(request, 'alumni_tracker/display.html', {'alumni_list': alumni_results})
		#return Alumnus.objects.all()

def display_self_profile(request):

	name =  request.GET.get("name")
	grad_year =  request.GET.get("grad_year")
	cgpa =  request.GET.get("cgpa")
	city =  request.GET.get("city")
	present_country = request.GET.get("present_country")
	dept_code =  request.GET.get("dept_code")
	email_id =  request.GET.get("email_id")
	roll_no =  request.GET.get("roll_no")
	company_name = request.GET.get("company_name")
	company_city = request.GET.get("company_city")
	school_city = request.GET.get("school_city")
	school_country = request.GET.get("school_country")
	school_name =  request.GET.get("school_name")
	school_grad = request.GET.get("school_grad")
	school_programme = request.GET.get("school_programme")
	job_field = request.GET.get("job_field")
	job_position = request.GET.get("job_position")
	github = request.GET.get("github")
	linkedin = request.GET.get("linkedin")
	major1 = request.GET.get("major1")
	major2 = request.GET.get("major2")

	try:
		if Alumnus.objects.get(pk=roll_no):
			return HttpResponse("Roll no exists")
	except ObjectDoesNotExist:
		try:
			p=Location.objects.only('city').get(city=city)
		except ObjectDoesNotExist:
			c=Location.objects.create(city=city,country=present_country)
			p=Location.objects.only('city').get(city=city)
		#q = Alumnus(alumni_name=name, roll_no=roll_no, present_city=Location.objects.get(pk=city).city, email_id=email_id, grad_year=grad_year, cgpa=cgpa)
		#q.save()
		try:
			p1=Location.objects.only('city').get(city=school_city)
		except ObjectDoesNotExist:
			c1=Location.objects.create(city=city,country=school_country)
			p1=Location.objects.only('city').get(city=school_city)
		try:
			p2=Location.objects.only('city').get(city=company_city)
		except ObjectDoesNotExist:
			c2=Location.objects.create(city=city,country=company_country)	
			p2=Location.objects.only('city').get(city=company_city)
		try:
			p3=Company.objects.only('name').get(name=company_name,city=company_city)
		except ObjectDoesNotExist:
			c3=Company.objects.create(name=company_name,city=company_city)
		try:
			p4=School.objects.only('school_name').get(school_name=school_name)
		except ObjectDoesNotExist:
			c4=School.objects.create(school_name=school_name,city=school_city)

		studied = Studied.objects.create(school_name=School.objects.only('school_name').get(school_name=school_name),roll_no=Alumnus.objects.only('roll_no').get(roll_no=roll_no), programme=school_programme, grad_year=school_grad)			
		job = Job.objects.create(roll_no=Alumnus.objects.only('roll_no').get(roll_no=roll_no), company_id=Company.objects.only('company_id').get(name=company_name),field=job_field, position=job_position)
		
		major = Alumnus_majors.objects.create(roll_no=Alumnus.objects.only('roll_no').get(roll_no=roll_no), major=major1)
		major = Alumnus_majors.objects.create(roll_no=Alumnus.objects.only('roll_no').get(roll_no=roll_no), major=major2)
		
		q=Alumnus.objects.create(alumni_name=name, roll_no=roll_no, present_city=p, email_id=email_id, grad_year=grad_year, cgpa=cgpa ,dept_code= Department.objects.only('dept_code').get(dept_code=dept_code),linkedin=linkedin,github=github)
		alumni = Alumnus.objects.get(pk=q.roll_no)
		print Alumnus.objects.only('email_id')
		context = {"alumnus" : alumni}
		return render(request,'alumni_tracker/display_self_profile.html',context)
	
def updatealumnus(request,pk):

	def get(self,request):
		form = self.form_class(None)

class AlumnusUpdate(UpdateView):
	model = Alumnus
	fields = ['alumni_name','roll_no','present_city','email_id','dept_code','grad_year','cgpa']

class AlumnusDelete(DeleteView):
	model = Alumnus
	success_url=reverse_lazy('alumni_tracker:home')

def home(request):
	context = {}
	return render(request, 'alumni_tracker/home.html',context)

def registration(request):
    return HttpResponse("Hello, world. You're at the registration page")

#def login(request):
 #   return HttpResponse("Hello, world. You can mnow login")

def search(request):
	all_alumni = Alumnus.objects.all()
	context = {}
	return render(request, 'alumni_tracker/search.html',context)

def createalumnus(request):
	context = {}
	return render(request,'alumni_tracker/createalumnus.html',context)

##THIS IS THE REGISTRATION PAGE
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
					login(request,user)
					return redirect('alumni_tracker:createalumnus')

		return render(request, self.template_name,{'form':form})

def register(request):
	user_form = UserForm
	alumni_form = AlumniForm
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
					login(request,user)
					return redirect('alumni_tracker:createalumnus')

		return render(request, self.template_name,{'form':form})


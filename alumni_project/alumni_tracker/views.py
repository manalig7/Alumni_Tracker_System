

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

def details(request,pk):
	alumnus = Alumnus.objects.get(roll_no=pk)
	department = Department.objects.get(dept_code=alumnus.dept_code)
	job = Job.objects.filter(roll_no=pk)
	school=Studied.objects.filter(roll_no=pk)
	majors=Alumnus_majors.objects.filter(roll_no=pk)
	#for jobs in job:
	#	company = Company.objects.filter(id=jobs.company_id)
	context = {'alumnus':alumnus,'department':department,'job':job,'school':school,'majors':majors}
	return render(request,'alumni_tracker/details.html',context)

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
	company_country = request.GET.get("company_country")
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
			return redirect('alumni_tracker:errorpage')

	except ObjectDoesNotExist:
		try:
			p=Location.objects.only('city').get(city=city,country=present_country)
		except ObjectDoesNotExist:
			c=Location.objects.create(city=city,country=present_country)#Creates the present location if it is not already present
			p=Location.objects.only('city').get(city=city,country=present_country)
		#q = Alumnus(alumni_name=name, roll_no=roll_no, present_city=Location.objects.get(pk=city).city, email_id=email_id, grad_year=grad_year, cgpa=cgpa)
		#q.save()
		#Creates the city in which the school is located if it is not already present
		try:
			p1=Location.objects.only('city').get(city=school_city,country=school_country)
		except ObjectDoesNotExist:
			c1=Location.objects.create(city=school_city,country=school_country)
			p1=Location.objects.only('city').get(city=school_city,country=school_country)
		#Creates the city in which the company is located if it is not already present
		try:
			p2=Location.objects.only('city').get(city=company_city,country=company_country)
		except ObjectDoesNotExist:
			c2=Location.objects.create(city=company_city,country=company_country)	
			p2=Location.objects.only('city').get(city=company_city,country=company_country)
		#Checks if the unique company+city entry is already present
		try:
			p3=Company.objects.only('name').get(name=company_name,city=company_city)
		except ObjectDoesNotExist:
			c3=Company.objects.create(name=company_name,city=p2)
		try:
			p4=School.objects.only('school_name').get(school_name=school_name,city=school_city)
		except ObjectDoesNotExist:
			c4=School.objects.create(school_name=school_name,city=p1)

		q=Alumnus.objects.create(alumni_name=name, roll_no=roll_no, present_city=p, email_id=email_id, grad_year=grad_year, cgpa=cgpa ,dept_code= Department.objects.only('dept_code').get(dept_code=dept_code),linkedin=linkedin,github=github)
		studied = Studied.objects.create(roll_no=Alumnus.objects.only('roll_no').get(roll_no=roll_no), school_name=School.objects.only('school_name').get(school_name=school_name),programme=school_programme, grad_year=school_grad)			
		job = Job.objects.create(roll_no=Alumnus.objects.only('roll_no').get(roll_no=roll_no), company_id=Company.objects.only('id').get(name=company_name,city=company_city),field=job_field, position=job_position)
		major = Alumnus_majors.objects.create(roll_no=Alumnus.objects.only('roll_no').get(roll_no=roll_no), major=major1)
		major = Alumnus_majors.objects.create(roll_no=Alumnus.objects.only('roll_no').get(roll_no=roll_no), major=major2)

		#Contexts
		majors = Alumnus_majors.objects.filter(roll_no=roll_no)
		alumni = Alumnus.objects.get(pk=q.roll_no)
		jobs = Job.objects.filter(roll_no=roll_no)
		company = Company.objects.filter(name=company_name)

		#print Alumnus.objects.only('email_id')
		context = {"alumnus" : alumni, "majors" : majors,"jobs" : jobs , "company" : company}
		return render(request,'alumni_tracker/display_self_profile.html',context)

def error(request):
	context = {}
	return render(request,'alumni_tracker/errorpage.html',context)

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


def login_user(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate (username = username,password= password)
		if user is not None:
			if user.is_active:
				login(request,user)
				alumnus = Alumnus.objects.get(roll_no=request.user)
				department = Department.objects.get(dept_code=alumnus.dept_code)
				school = Studied.objects.get(roll_no=alumnus.roll_no)
				company=Job.objects.filter(roll_no=alumnus.roll_no)
				majors=Alumnus_majors.objects.filter(roll_no=alumnus.roll_no)
				context = {
					'alumnus':alumnus,
					'department':department,
					'school':school,
					'company':company,
					'majors': majors,
		
				}
				return render(request,'alumni_tracker/home.html',context)
			else:
				return render(request,'alumni_tracker/login.html',{'error_message':'Your account has been disabled'})

		else:
			return render(request,'alumni_tracker/login.html',{'error_message':'Invalid login'})
	return render(request,'alumni_tracker/login.html')

def update_home(request):
	context={}
	return render(request,'alumni_tracker/update_home.html',context)

def updateprofile_new(request):
	form = UpdateProfileForm(request.POST or None)
	alumnus = Alumnus.objects.get(roll_no = request.user)
	if form.is_valid() and request.method== "POST":
		
		roll_no = request.POST["roll_no"]
		sem = request.POST["sem"]
		hostel = request.POST["hostel_block"]
		hostel_inst = Hostel_block.objects.get(block_no=hostel)
		branch = request.POST["branch"]
		mess_names = request.POST["mess_names"]
		mess_name = Mess.objects.get(mess_name=mess_names)
		
		student.sem = sem
		student.hostel_block = hostel_inst
		student.branch = branch

		student.mess_names = mess_name
		student.save()
		student = Student.objects.get(user=request.user)
		room = Room.objects.get(room_no = str(student.room_no))
		hostel = Hostel_block.objects.get(block_no = str(room.block_no))

		mess = Mess.objects.get(mess_name = student.mess_names)
		
		context = {
			'student':student,
			'room':room,
			'hostel':hostel,
			'mess':mess,
			'roll_no': student.roll_no,
		
		}
		return render(request,'info/index.html',context)
	else:
		context = {
					'form' : form,
		}
		return render(request,'info/update_profile.html',context)

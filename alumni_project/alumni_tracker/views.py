

from django.http import HttpResponse
from django.shortcuts import render,redirect
from .models import Location, Alumnus, School, Department, Company, Studied, Job, Alumnus_majors
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView   #to create,edit a new object
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import authenticate, login, logout    
from django.views.generic import View
from .forms import UserForm,UpdateProfileForm
from django.db.models import Q
from django.contrib.auth import views as auth_views
from django.core.exceptions import ObjectDoesNotExist


#Shows details of the alumni searched
def details(request,pk):
	majors = Alumnus_majors.objects.filter(roll_no=pk)
	alumni = Alumnus.objects.get(roll_no=pk)
	jobs = Job.objects.filter(roll_no=pk)
	lj=[]
	for obj in jobs:
		lj.append(obj.company_id)
	lj1=[]
	for obj in lj:
		lj1.append(obj.pk)
	company = Company.objects.filter(pk__in=lj1)
	studied_list = Studied.objects.filter(roll_no=pk)
	ls=[]
	for obj in studied_list:
		ls.append(obj.school_name)
	school = School.objects.filter(school_name__in=ls)
	fields = []
	positions =[]
	companies = []
	company_cities = []
	for obj in jobs:
		fields.append(obj.field)
		positions.append(obj.position)
	for obj in company:
		companies.append(obj.name)
		company_cities.append(obj.city)

	schools = []
	grad_years =[]
	programmes = []
	
	
	for obj in studied_list:
		programmes.append(obj.programme)
		grad_years.append(obj.grad_year)
		schools.append(obj.school_name)

	work = zip(fields,positions,companies,company_cities)
	edu = zip(schools,grad_years,programmes)
	context = {"alumnus" : alumni, "majors" : majors,"jobs" : jobs , "company" : company , 'school' : school, 'studied_list' : studied_list, 'fields' : fields, 'positions':positions, 'companies' : companies,'work':work,'edu':edu}

	return render(request,'alumni_tracker/details.html',context)

#Displays the list of alumni satisfying the search filters
def display(request):
	alumni_results = Alumnus.objects.all()
	name = request.GET.get("name")
	grad_year= request.GET.get("grad_year")
	present_city= request.GET.get("present_city")
	dept_code= request.GET.get("dept_code")
	school_name= request.GET.get("school_name")
	company_name= request.GET.get("company_name")

	flag=1
	if name:
		alumni_results = alumni_results.filter(
			Q(alumni_name__icontains=name) 
		).distinct()
	if grad_year:
		alumni_results = alumni_results.filter(
		Q(grad_year__exact=grad_year) 
	).distinct()
	if present_city:
		alumni_results = alumni_results.filter(
		Q(present_city__city__icontains=present_city) 
	).distinct()
	if dept_code:
		alumni_results = alumni_results.filter(
		Q(dept_code__dept_code__icontains=dept_code) 
	).distinct()
	if school_name:
		ls=[]
		ls1=[]
		schools=School.objects.only('school_name').all().filter(school_name__contains=school_name)
		for obj in schools:
			ls1.append(obj.school_name)
		studied = Studied.objects.only('roll_no').all().filter(school_name__in=ls1)
		for obj in studied:
			ls.append(obj.roll_no.roll_no)
		alumni_results=alumni_results.filter(roll_no__in=ls).distinct()
		 
	if company_name:
		ls=[]
		ls1=[]
		companies=Company.objects.only('id').filter(name__contains=company_name)
		for obj in companies:
			ls1.append(obj.id)
		jobs = Job.objects.only('roll_no').filter(company_id__in=ls1)	
		for obj in jobs:
			ls.append(obj.roll_no.roll_no)
		alumni_results=alumni_results.filter(roll_no__in=ls).distinct()
	if flag==1:
		return render(request, 'alumni_tracker/display.html', {'alumni_list': alumni_results})
	else:
		return render(request, 'alumni_tracker/display.html', {'alumni_list': alumni_results})

#Displays your own profile if logged in
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
			if city:
				return redirect('alumni_tracker:errorpage')
			else:
				#Creates the city in which the school is located if it is not already present
				if school_city and school_country and school_name:
					try:
						p1=Location.objects.only('city').get(city=school_city,country=school_country)
					except ObjectDoesNotExist:
						c1=Location.objects.create(city=school_city,country=school_country)
						p1=Location.objects.only('city').get(city=school_city,country=school_country)
					#Creates the school if not already present
					try:
						p4=School.objects.only('school_name').get(school_name=school_name,city=school_city)
					except ObjectDoesNotExist:
						c4=School.objects.create(school_name=school_name,city=p1)
						p4=School.objects.only('school_name').get(school_name=school_name,city=school_city)
					
					studied = Studied.objects.create(roll_no=Alumnus.objects.only('roll_no').get(roll_no=roll_no), school_name=p4,programme=school_programme, grad_year=school_grad)			
				

				#Creates the city in which the company is located if it is not already present
				if company_city and company_country and company_name:
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
						job = Job.objects.create(roll_no=Alumnus.objects.only('roll_no').get(roll_no=roll_no), company_id=Company.objects.only('id').get(name=company_name,city=company_city),field=job_field, position=job_position)

				majors = Alumnus_majors.objects.filter(roll_no=roll_no)
				alumni = Alumnus.objects.get(pk=roll_no)
				jobs = Job.objects.filter(roll_no=roll_no)
				lj=[]
				for obj in jobs:
					lj.append(obj.company_id)
				lj1=[]
				for obj in lj:
					lj1.append(obj.pk)
				company = Company.objects.filter(pk__in=lj1)
				studied_list = Studied.objects.filter(roll_no=roll_no)
				ls=[]
				for obj in studied_list:
					ls.append(obj.school_name)
				school = School.objects.filter(school_name__in=ls)
				#print Alumnus.objects.only('email_id')
				schools =[]
				grad_years=[]
				programmes=[]
				
				
				for obj in studied_list:
					grad_years.append(obj.grad_year)
					programmes.append(obj.programme)
					schools.append(obj.school_name)

				edu = zip(schools,grad_years,programmes)

				fields = []
				positions =[]
				companies = []
				company_cities = []
				for obj in jobs:
					fields.append(obj.field)
					positions.append(obj.position)
				for obj in company:
					companies.append(obj.name)
					company_cities.append(obj.city)
				work = zip(fields,positions,companies,company_cities)

				context = {"alumnus" : alumni, "majors" : majors,"jobs" : jobs , "company" : company , 'school' : school, 'studied_list' : studied_list,'edu':edu, 'work' :work}
				return render(request,'alumni_tracker/display_self_profile.html',context)


	except ObjectDoesNotExist:
		if present_country and city:
			try:
				p=Location.objects.only('city').get(city=city,country=present_country)
			except ObjectDoesNotExist:

				c=Location.objects.create(city=city,country=present_country)#Creates the present location if it is not already present
				p=Location.objects.only('city').get(city=city,country=present_country)

		q=Alumnus.objects.create(alumni_name=name, roll_no=roll_no, present_city=Location.objects.only('city').get(city=city,country=present_country), email_id=email_id, grad_year=grad_year, cgpa=cgpa ,dept_code= Department.objects.only('dept_code').get(dept_code=dept_code),linkedin=linkedin,github=github)
		majors = Alumnus_majors.objects.filter(roll_no=roll_no)

		if school_city and school_country and school_name:	
			try:
				p2=Location.objects.only('city').get(city=school_city,country=school_country)
			except ObjectDoesNotExist:
				c2=Location.objects.create(city=school_city,country=school_country)	
				p2=Location.objects.only('city').get(city=school_city,country=school_country)
			try:
				p3=School.objects.only('school_name').get(school_name=school_name,city=school_city)
			except ObjectDoesNotExist:
				c3=School.objects.create(school_name=school_name,city=p2)
			studied = Studied.objects.create(roll_no=Alumnus.objects.only('roll_no').get(roll_no=roll_no), school_name=School.objects.only('school_name').get(school_name=school_name,city=school_city),grad_year=school_grad, programme=school_programme)

			#Creates the city in which the company is located if it is not already present
		if company_city and company_country and company_name:	
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
			job = Job.objects.create(roll_no=Alumnus.objects.only('roll_no').get(roll_no=roll_no), company_id=Company.objects.only('id').get(name=company_name,city=company_city),field=job_field, position=job_position)

		major = Alumnus_majors.objects.create(roll_no=Alumnus.objects.only('roll_no').get(roll_no=roll_no), major=major1)
		major = Alumnus_majors.objects.create(roll_no=Alumnus.objects.only('roll_no').get(roll_no=roll_no), major=major2)

		#Contexts
		majors = Alumnus_majors.objects.filter(roll_no=roll_no)
		alumni = Alumnus.objects.get(pk=q.roll_no)
		jobs = Job.objects.filter(roll_no=roll_no)
		company = Company.objects.filter(name=company_name,city=company_city)

		studied_list = Studied.objects.filter(roll_no=roll_no)
		ls=[]
		for obj in studied_list:
			ls.append(obj.school_name)
		school = School.objects.filter(school_name__in=ls)
		schools =[]
		grad_years=[]
		programmes=[]
		
		for obj in studied_list:
			grad_years.append(obj.grad_year)
			programmes.append(obj.programme)
			schools.append(obj.school_name)

		edu = zip(schools,grad_years,programmes)

		fields = []
		positions =[]
		companies = []
		company_cities = []
		for obj in jobs:
			fields.append(obj.field)
			positions.append(obj.position)
		for obj in company:
			companies.append(obj.name)
			company_cities.append(obj.city)
		work = zip(fields,positions,companies,company_cities)

		context = {"alumnus" : alumni, "majors" : majors,"jobs" : jobs , "company" : company , 'school' : school, 'studied_list' : studied_list, 'work':work, 'edu':edu}
		return render(request,'alumni_tracker/display_self_profile.html',context)


def error(request):
	context = {}
	return render(request,'alumni_tracker/errorpage.html',context)

# To update your alumnus profile
def updatealumnus(request,pk):

	def get(self,request):
		form = self.form_class(None)

# Home page
def home(request):
	context = {}
	return render(request, 'alumni_tracker/home.html',context)

# Search page
def search(request):
	all_alumni = Alumnus.objects.all()
	context = {}
	return render(request, 'alumni_tracker/search.html',context)

#
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
				alumni = Alumnus.objects.get(roll_no=user)
				roll_no = user
				majors = Alumnus_majors.objects.filter(roll_no=alumni.roll_no)
				jobs = Job.objects.filter(roll_no=alumni.roll_no)
				ls1=[]
				ls2=[]
				studied_list = Studied.objects.all().filter(roll_no=alumni.roll_no)
				ls=[]
				for obj in studied_list:
					ls.append(obj.school_name)
				school = School.objects.filter(school_name__in=ls)
				lc=[]
				compid_list = Job.objects.all().filter(roll_no=alumni.roll_no)
				for obj in compid_list:
					lc.append(obj.company_id)
				lc1=[]
				for obj in lc:
					lc1.append(obj.id)
				company = Company.objects.filter(id__in=lc1)
				schools =[]
				grad_years=[]
				programmes=[]
				
				for obj in studied_list:
					grad_years.append(obj.grad_year)
					programmes.append(obj.programme)
					schools.append(obj.school_name)

				edu = zip(schools,grad_years,programmes)

				fields = []
				positions =[]
				companies = []
				company_cities = []
				for obj in jobs:
					fields.append(obj.field)
					positions.append(obj.position)
				for obj in company:
					companies.append(obj.name)
					company_cities.append(obj.city)
				work = zip(fields,positions,companies,company_cities)
				context = {"alumnus" : alumni, "majors" : majors,"jobs" : jobs , "company" : company , 'school' : school, 'studied_list' : studied_list, 'edu':edu, 'work':work}
				return render(request,'alumni_tracker/display_self_profile.html',context)
			else:
				return render(request,'alumni_tracker/login.html',{'error_message':'Your account has been disabled'})
		else:
			return render(request,'alumni_tracker/login.html',{'error_message':'Invalid login'})
	return render(request,'alumni_tracker/login.html')



def updateprofile_new(request,pk):
	form = UpdateProfileForm(request.POST or None)
	alumnus = Alumnus.objects.get(roll_no = pk)
	if form.is_valid() and request.method== "POST":
		roll_no = request.POST["roll_no"]
		present_city=request.POST["present_city"]
		present_country=request.POST["present_country"]
		email_id=request.POST["email_id"]
		github=request.POST["github"]
		linkedin=request.POST["linkedin"]
		alumnus.present_city = Location.objects.only('city').get(city=present_city)
		alumnus.email_id=email_id
		alumnus.linkedin=linkedin
		alumnus.github=github
		alumnus.save()
		alumnus = Alumnus.objects.get(roll_no=pk)
		dept = Department.objects.get(dept_code=alumnus.dept_code)
		job = Job.objects.filter(roll_no=alumnus.roll_no)
		studied = Studied.objects.filter(roll_no=alumnus.roll_no)
		majors = Alumnus_majors.objects.filter(roll_no=alumnus.roll_no)
		context = {'alumnus': alumnus,'dept':dept,'jobs': job ,'studied' : studied,'majors' : majors}
		return render(request,'alumni_tracker/display_self_profile.html',context)
	else:
		context = {'form' : form,'alumnus':alumnus}
		return render(request,'alumni_tracker/update_profile.html',context)


def add_schools_success(request,pk):

	alumnus = Alumnus.objects.get(roll_no=pk)
	school_city = request.GET.get("school_city")
	school_country = request.GET.get("school_country")
	school_name =  request.GET.get("school_name")
	school_grad = request.GET.get("school_grad")
	school_programme = request.GET.get("school_programme")
	
	try:
		p=Location.objects.only('city').get(city=school_city,country=school_country)
	except ObjectDoesNotExist:
		c=Location.objects.create(city=school_city,country=school_country)
		p=Location.objects.only('city').get(city=school_city,country=school_country)

	try:
		p1=School.objects.get(school_name=school_name)
	except ObjectDoesNotExist:
		c1=School.objects.create(school_name=school_name,city=p)
		p1=School.objects.only('school_name').get(school_name=school_name)

	rno = Alumnus.objects.only('roll_no').get(roll_no=pk)
	c2=Studied.objects.create(roll_no=rno,school_name=p1,grad_year=school_grad,programme=school_programme)


	context = {'alumnus':alumnus}
	return render(request, 'alumni_tracker/add_schools_success.html',context)

def update_profile_success(request,pk):

	alumnus = Alumnus.objects.get(roll_no=pk)
	present_city = request.GET.get("present_city")
	present_country = request.GET.get("present_country")
	email_id =  request.GET.get("email_id")
	github = request.GET.get("github")
	linkedin = request.GET.get("linkedin")
	name = request.GET.get("name")
	
	if present_city:
		try:
			p=Location.objects.only('city').get(city=present_city,country=present_country)
		except ObjectDoesNotExist:
			c=Location.objects.create(city=present_city,country=present_country)
			p=Location.objects.only('city').get(city=present_city,country=present_country)

	if name:
		alumnus.alumni_name = name
	if present_city:
		alumnus.present_city = p
	if email_id:
		alumnus.email_id = email_id
	if github:
		alumnus.github = github
	if linkedin:
		alumnus.linkedin = linkedin
	alumnus.save()
	alumnus = Alumnus.objects.get(roll_no=pk)
	context = {'alumnus':alumnus}
	return render(request, 'alumni_tracker/update_profile_success.html',context)

def add_majors_success(request,pk):

	alumnus = Alumnus.objects.get(roll_no=pk)
	roll_no = request.GET.get("roll_no")
	major = request.GET.get("major")
	
	c = Alumnus_majors.objects.create(roll_no=Alumnus.objects.only('roll_no').get(roll_no=pk),major=major)
	
	context = {'alumnus':alumnus}
	return render(request, 'alumni_tracker/add_majors_success.html',context)


def createschool(request,pk):
	alumnus = Alumnus.objects.get(roll_no=pk)
	context = {'alumnus':alumnus}
	return render(request,'alumni_tracker/createschool.html',context)

def updateprofile_new(request,pk):
	alumnus = Alumnus.objects.get(roll_no=pk)
	context = {'alumnus':alumnus}
	return render(request,'alumni_tracker/update_profile.html',context)

def createmajor(request,pk):
	alumnus = Alumnus.objects.get(roll_no=pk)
	context = {'alumnus':alumnus}
	return render(request,'alumni_tracker/createmajor.html',context)


def createcompany(request,pk):
	alumnus = Alumnus.objects.get(roll_no=pk)
	context = {'alumnus': alumnus}
	return render(request,'alumni_tracker/createcompany.html',context)

def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return redirect('alumni_tracker:home')
def add_company_success(request,pk):

	alumnus = Alumnus.objects.get(roll_no=pk)
	company_city = request.GET.get("company_city")
	company_country = request.GET.get("company_country")
	company_name =  request.GET.get("company_name")
	field = request.GET.get("job_field")
	position = request.GET.get("job_position")
	
	try:
		p=Location.objects.only('city').get(city=company_city,country=company_country)
	except ObjectDoesNotExist:
		c=Location.objects.create(city=company_city,country=company_country)
		p=Location.objects.only('city').get(city=company_city,country=company_country)

	try:
		p1=Company.objects.get(name=company_name,city=company_city)
	except ObjectDoesNotExist:
		c1=Company.objects.create(name=company_name,city=p)
		p1=Company.objects.only('id').get(name=company_name,city=company_city)

	rno = Alumnus.objects.only('roll_no').get(roll_no=pk)
	c2=Job.objects.create(roll_no=rno,company_id=p1,field=field,position=position)


	context = {'alumnus':alumnus}
	return render(request, 'alumni_tracker/create_company_success.html', context)


"""class IndexView(generic.ListView):
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

		return render(self, 'alumni_tracker/display.html', {'alumni': alumni})"""	
"""class DetailView(generic.DetailView):
	model = Alumnus
	template_name = 'alumni_tracker/details.html'
	context_object_name = 'alumnus'"""

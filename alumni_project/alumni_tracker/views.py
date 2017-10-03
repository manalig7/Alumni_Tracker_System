

from django.http import HttpResponse
from django.template import loader
from .models import Location, Alumnus, School, Department, Company, Studied, Job, Alumnus_majors, Alumnus_links

def home(request):
	html = '<a href="/alumni_tracker/login/">Login</a><br> <a href="/alumni_tracker/registration/">Registration</a><br> <a href="/alumni_tracker/search/">Search</a><br>'
	return HttpResponse(html)

def registration(request):
    return HttpResponse("Hello, world. You're at the registration page")

def login(request):
    return HttpResponse("Hello, world. You can mnow login")

def search(request):
	all_alumni = Alumnus.objects.all()
	html = ''
	for alumnus in all_alumni:
		url = '/alumni_tracker/search/' + alumnus.roll_no + '/'
		html += '<a href="' + url + '">' + alumnus.alumni_name + '</a><br>'
	return HttpResponse(html)

def details(request,alumnus_id):
    return HttpResponse("Hello, world. You're at the details page for alumnus" + alumnus_id)



# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Location, Alumnus, School, Department, Company, Studied, Job, Alumnus_majors
# Register your models here.
admin.site.register(Location)
admin.site.register(Alumnus)
admin.site.register(School)
admin.site.register(Department)

admin.site.register(Company)
admin.site.register(Studied)

admin.site.register(Job)
admin.site.register(Alumnus_majors)


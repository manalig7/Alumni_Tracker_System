from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views
app_name = 'alumni_tracker'

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^registration/$',views.UserFormView.as_view(), name="registration"),
    url(r'^login/$',views.login_user, name="login"),
    url(r'^search/$',views.search, name="search"),
    #url(r'^search/(?P<alumnus_id>[0-9]+[A-Z]+[0-9]+)/$',views.details, name="details"),
    url(r'^search/display/$', views.display, name='display'),
    url(r'^search/display/(?P<pk>[0-9]+[A-Z]+[0-9]+)/$', views.details, name='details'),
    url(r'^createalumnus/$',views.createalumnus,name='createalumnus'),
    url(r'^updatealumnus/(?P<pk>[0-9]+[A-Z]+[0-9]+)/$',views.updateprofile_new,name='updatealumnus'),
    url(r'^deletealumnus/(?P<pk>[0-9]+[A-Z]+[0-9]+)/$',views.AlumnusDelete.as_view(),name='deletealumnus'),
    url(r'^display_self_profile/$',views.display_self_profile,name = 'display_self_profile'),
    url(r'^errorpage', views.error,name='errorpage'),
    url(r'^createschool/(?P<pk>[0-9]+[A-Z]+[0-9]+)/$',views.createschool,name='createschool'),
    url(r'^add_schools_success/(?P<pk>[0-9]+[A-Z]+[0-9]+)/$',views.add_schools_success,name='add_schools_success'),
    url(r'^logout/$',views.logout_user, name="logout"),
    url(r'^createcompany/(?P<pk>[0-9]+[A-Z]+[0-9]+)/$',views.createcompany,name='createcompany'),
    url(r'^add_company_success/(?P<pk>[0-9]+[A-Z]+[0-9]+)/$',views.add_company_success,name='add_company_success'),
    
]

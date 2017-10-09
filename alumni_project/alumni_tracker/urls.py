from django.conf.urls import url

from . import views
app_name = 'alumni_tracker'

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^registration/$',views.UserFormView.as_view(), name="registration"),
    url(r'^login/$',views.login, name="login"),
    url(r'^search/$',views.search, name="search"),
    #url(r'^search/(?P<alumnus_id>[0-9]+[A-Z]+[0-9]+)/$',views.details, name="details"),
    url(r'^search/display/$', views.display, name='display'),
    url(r'^search/display/(?P<pk>[0-9]+[A-Z]+[0-9]+)/$', views.DetailView.as_view(), name='details'),
    url(r'^createalumnus/$',views.AlumnusCreate.as_view(),name='createalumnus'),
]

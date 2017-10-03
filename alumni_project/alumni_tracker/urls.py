from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^registration/$',views.registration, name="registration"),
    url(r'^login/$',views.login, name="login"),
    url(r'^search/$',views.search, name="search"),
    url(r'^search/(?P<alumnus_id>[0-9]+[A-Z]+[0-9]+)/$',views.details, name="details"),
]

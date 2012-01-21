from django.conf.urls.defaults import *

from django.views.generic import TemplateView
    
# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()


urlpatterns = patterns('',
                       
    (r'^$', TemplateView.as_view(template_name="bootstrap.html")),

	(r'about/$', TemplateView.as_view(template_name="about.html")),

   	(r'contact/$', TemplateView.as_view(template_name="comingsoon.html")),
    # Example:
#    (r'^aim/', include('aim.urls') ),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout'),

    # Uncomment the next line to enable the admin:
#    (r'^admin/(.*)', admin.site.root),
)

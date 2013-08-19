from django.conf.urls.defaults import patterns, include, url
from django.views.generic import TemplateView

class BootstrapSampleView(TemplateView):
    template_name = "sample.html"
    

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'aim_v13.views.home', name='home'),
    # url(r'^aim_v13/', include('aim_v13.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^bootstrap/', BootstrapSampleView.as_view()),
    
    #url(r'^aim/', include(aim.urls) ),
    
    url(r'^$', TemplateView.as_view(template_name = "index.html") ),
    
)
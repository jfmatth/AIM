from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'finance.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', TemplateView.as_view(template_name = "index.html") ),
    
    url(r'^aim/', include('aim.urls')),
    
    url(r'^loader/', include('loader.urls')),
    
    url(r'^graph/', include('graphs.urls')),

    url(r'^admin/', include(admin.site.urls)),
    
    (r'^accounts/', include('registration.backends.default.urls')), # django registration
)

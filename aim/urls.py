 # aim.urls.py
 
from django.conf.urls.defaults import *

from aim.views import IndexView

urlpatterns = patterns('',
#    (r'^$',                                         'aim.views.index'),
    (r'^$', IndexView.as_view() ),

    (r'^login/$',                                   'aim.views.aim_login'),

    # Portfolio
    (r'^portfolio/(?P<portfolio_id>\d+)/$',        'aim.views.portfolio'),
    (r'^portfolio/add/$',                          'aim.views.portfolio_add'),
    (r'^portfolio/edit/(?P<portfolio_id>\d+)/$',   'aim.views.portfolio_edit'),
    
    # Holdings
    (r'^holding/all/$',                            'aim.views.holding_all'),
    (r'^holding/(?P<holding_id>\d+)/$',            'aim.views.holding'),
    (r'^holding/add/$',                            'aim.views.holding_add'),
    (r'^holding/edit/(?P<holding_id>\d+)/$',       'aim.views.holding_edit'),
    
)

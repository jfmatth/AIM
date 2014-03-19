 # aim.urls.py
 
from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from aim.views import MainView, PortfolioUpdate, PortfolioCreate, HoldingCreateView, TransactionCreate
from aim.views import HoldingUpdateView, PriceView 

urlpatterns = patterns('',
    url(r'^$',
        login_required(MainView.as_view() ),
        name = "main"
    ),

    # Portfolio URL's
    url(r'^portfolio/(?P<pk>\d+)/$',
        login_required(PortfolioUpdate.as_view()),
        name = "portfolio_edit" ),
    url(r'^portfolio/add/$',
        login_required(PortfolioCreate.as_view()),
        name = "portfolio_add" ),

    # Holding URL's
    url(r'^holding/add/(?P<portid>\d+)/$',
        login_required(HoldingCreateView.as_view()),
        name = "holding_add"),
    url(r'^holding/add/$',
        login_required(HoldingCreateView.as_view()),
        name = "holding_addplain"),
    url(r'^holding/(?P<pk>\d+)/$',
        login_required(HoldingUpdateView.as_view()),
        name = "holding_view"),
             
    
    # Transaction URL's
    url(r'^transaction/(?P<holding_id>\d+)/$',
        login_required(TransactionCreate.as_view() ),
        name = "transaction"),
                       
    url(r'price/(?P<holding_id>\d+)/$', PriceView.as_view() ),
    
    url(r'^graphdata/', TemplateView.as_view(template_name="aim/graphdata.html")),

                       
#     (r'^portfolio/add/$',                          'aim.views.portfolio_add'),
#     (r'^portfolio/edit/(?P<portfolio_id>\d+)/$',   'aim.views.portfolio_edit'),
    
    # Holdings
#     (r'^holding/all/$',                            'aim.views.holding_all'),
#     (r'^holding/(?P<holding_id>\d+)/$',            'aim.views.holding'),
#     (r'^holding/add/$',                            'aim.views.holding_add'),
#     (r'^holding/edit/(?P<holding_id>\d+)/$',       'aim.views.holding_edit'),
    
)
    